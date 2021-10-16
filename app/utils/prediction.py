import io
import os, sys
import pickle

from PIL import Image
import torchvision.models as models
import torch
import torchvision.transforms as transforms 


with open('./app/utils/id2class.pkl', 'rb') as f:
    id2class = pickle.load(f)

model = models.mobilenet_v3_small()
checkpoint = 'https://drive.google.com/u/0/uc?id=1A2ML5IpdYkTX88O--Jd0KnKC93ys2o0Z&export=download'
model.load_state_dict(torch.hub.load_state_dict_from_url(checkpoint, progress=False))
# model.load_state_dict(torch.load('./weights/mobilenet_v3_small-047dcff4.pth')) # In Local
model.eval()

transform = transforms.Compose([transforms.Resize((224,224)),
                                transforms.ToTensor(),
                                transforms.Normalize(mean = (0.485, 0.456, 0.406), std = (0.229, 0.224, 0.225))
                                ])

def get_top5(image_bytes):
    trans_imgs = []
    for image_byt in image_bytes:
        img = Image.open(io.BytesIO(image_byt))
        trans_imgs.append(transform(img))
    batch = torch.stack(trans_imgs, dim=0)
    with torch.no_grad():
        out = model(batch).softmax(dim=-1)  
    
    out = torch.topk(out, k=5, dim=-1)
    out_val, out_ind = out.values, out.indices
    result = {}
    
    for idx, (val, ind) in enumerate(zip(out_val, out_ind)):
        # Give top 5* predictions, with percentage. *Only if probability is above 1%.
        result[idx] = [( id2class[i.item()].split(',')[0], f'{v.item()*100:.2f}%' ) for i, v in zip(ind, val) if v.item() > 0.01]

    return result