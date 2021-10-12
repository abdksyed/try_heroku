import torchvision.models as models
import torch
import pickle
from PIL import Image
import torchvision.transforms as transforms 
import io

with open('./id2class.pkl', 'rb') as f:
    id2class = pickle.load(f)

model = models.mobilenet_v3_small()
# checkpoint = 'https://drive.google.com/u/0/uc?id=1A2ML5IpdYkTX88O--Jd0KnKC93ys2o0Z&export=download'
# model.load_state_dict(torch.hub.load_state_dict_from_url(checkpoint, progress=False))
model.load_state_dict(torch.load('./weights/mobilenet_v3_small-047dcff4.pth'))
model.eval()

transform = transforms.Compose([transforms.Resize((224,224)),
                                transforms.ToTensor(),
                                transforms.Normalize(mean = (0.485, 0.456, 0.406), std = (0.229, 0.224, 0.225))
                                ])

def get_top5(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    with torch.no_grad():
        out = model(transform(img).unsqueeze(0)).softmax(dim=-1)  
    out = out.topk(5)
    prob, idx = (out.values[0])*100, out.indices[0]
    classes = [id2class[i] for i in idx.tolist()]

    return prob.tolist(), classes