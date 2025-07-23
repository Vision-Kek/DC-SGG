import os
import torch
import torchvision


class GDINOStructure:
    def __init__(self, model, tokenizer, text_threshold, box_threshold, device):
        self.model = model
        self.tokenizer = tokenizer
        self.text_threshold = text_threshold
        self.box_threshold = box_threshold
        self.device = device


# create_positive_map_from_span is copied from original gdino code
def create_positive_map_from_span(tokenized, token_span, max_text_len=256):
    """construct a map such that positive_map[i,j] = True iff box i is associated to token j
    Input:
        - tokenized:
            - input_ids: Tensor[1, ntokens]
            - attention_mask: Tensor[1, ntokens]
        - token_span: list with length num_boxes.
            - each item: [start_idx, end_idx]
    """
    positive_map = torch.zeros((len(token_span), max_text_len), dtype=torch.float)
    for j, tok_list in enumerate(token_span):
        for (beg, end) in tok_list:
            beg_pos = tokenized.char_to_token(beg)
            end_pos = tokenized.char_to_token(end - 1)
            if beg_pos is None:
                try:
                    beg_pos = tokenized.char_to_token(beg + 1)
                    if beg_pos is None:
                        beg_pos = tokenized.char_to_token(beg + 2)
                except:
                    beg_pos = None
            if end_pos is None:
                try:
                    end_pos = tokenized.char_to_token(end - 2)
                    if end_pos is None:
                        end_pos = tokenized.char_to_token(end - 3)
                except:
                    end_pos = None
            if beg_pos is None or end_pos is None:
                continue

            assert beg_pos is not None and end_pos is not None
            if os.environ.get("SHILONG_DEBUG_ONLY_ONE_POS", None) == "TRUE":
                positive_map[j, beg_pos] = 1
                break
            else:
                positive_map[j, beg_pos: end_pos + 1].fill_(1)

    return positive_map / (positive_map.sum(-1)[:, None] + 1e-6)

def get_token_spans(query_string, phrase_delimter="."):
    gtoken_spans = []
    for phrase in query_string.split(phrase_delimter):
        if len(phrase) == 0: continue
        startpos = query_string.find(phrase)
        endpos = startpos + len(phrase)
        gtoken_spans.append([[startpos, endpos]])  # 1st [] for words 2nd [] for char
    return gtoken_spans

def cxcywh2xyxy(boxes, image_size):
    src_w, src_h = image_size
    boxes = boxes * torch.Tensor([src_w, src_h, src_w, src_h]).to(boxes.device)
    return torchvision.ops.box_convert(
        boxes=boxes,
        in_fmt="cxcywh",
        out_fmt="xyxy",
    )

def ensure_pil(img):
    if "pil" in str(type(img)).lower():
        return img
    else:
        return transforms.ToPILImage()(img)

def postprocess_gdino_villain_style(model_conf, outputs,
                                    batch):  # caption, tokenizer, token_spans, box_threshold, device
    caption, token_spans = batch["caption"], batch["token_spans"]
    tokenizer, box_threshold, device = model_conf.tokenizer, model_conf.box_threshold, model_conf.device
    logits = outputs.logits.sigmoid()[
        0]  # [boxes x tokens] , called logits, but actually it's always positive, not summing to 1 however (thus no probab)
    boxes = outputs.pred_boxes[0]  # [boxes x 4]

    positive_maps = create_positive_map_from_span(
        tokenizer(caption),
        token_span=token_spans  # [captions]
    ).to(
        device)  # [captions x tokens], for every caption, which tokens correspond to it (just according to the token span), sums to 1
    # print(f"{logits.shape=},{boxes.shape=},{positive_maps.shape=}")

    logits_for_phrases = positive_maps @ logits.T  # [captions x tokens] @ [tokens x boxes] , like a masking cuz most entries in positive_maps are =0
    all_logits = []
    all_phrases = []
    all_boxes = []
    for (token_span, logit_phr) in zip(token_spans, logits_for_phrases):
        phrase = ' '.join([caption[_s:_e] for (_s, _e) in token_span])
        filt_mask = logit_phr > box_threshold  # logit_phr [captions x boxes] ; filt_mask [boxes]
        all_boxes.append(boxes[filt_mask])
        all_logits.extend(logit_phr[filt_mask])

        logit_phr_num = logit_phr[filt_mask]
        all_phrases.extend([phrase for _ in logit_phr_num])

    boxes_filt = torch.cat(all_boxes, dim=0).cpu()

    # convert box format
    res_boxes = cxcywh2xyxy(boxes_filt, ensure_pil(batch["image"]).size)
    all_logits = torch.stack(all_logits if len(all_logits) > 0 else [torch.tensor([])], 0)

    return res_boxes, all_phrases, all_logits