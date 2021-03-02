import re
import sys
import functools
sys.path.append('../clip/')
import torch
from clip import clip
from model_tools.activations.pytorch import PytorchWrapper
from model_tools.activations.pytorch import load_preprocess_images
from model_tools.check_submission import check_models


all_models = ['ViT-B/32', 'RN50']
CLIP_RN50_LAYERS = ['layer1.0.relu', 'layer1.1.relu', 'layer1.2.relu'] +\
                  ['layer2.0.relu', 'layer2.1.relu', 'layer2.2.relu',
                   'layer2.3.relu'] +\
                   ['layer3.0.relu',  'layer3.1.relu', 'layer3.2.relu',
                    'layer3.3.relu', 'layer3.4.relu', 'layer3.5.relu'] +\
                    ['layer4.0.relu', 'layer4.1.relu', 'layer4.2.relu']


def get_model_list():
    return all_models

def get_model(name):
    assert name in all_models
    model, preprocess = clip.load(name, jit=False)
    model = model.visual
    for n, m in model.named_modules():
        print(n)
    # CLIP doesn't have nn.Module for projection head,
    # adding one to be compatible with BrainScore and
    # set the model.proj to the weights
    if name == 'ViT-B/32':
        feature_dim = 768
    elif name == 'RN50':
        feature_dim = 2048
        
    proj_weights = model.proj    
    model.ln_proj = torch.nn.Linear(feature_dim, model.output_dim)
    model.ln_proj.weights = proj_weights
    model.ln_proj.bias = torch.nn.Parameter(torch.zeros(model.output_dim))
    # add a ImageNet prediction head
    model.ln_pred = torch.nn.Linear(model.output_dim, 1000)
    # cast all weights from HalfTensors to FloatTensor    
    model.to(torch.float32, non_blocking=False)
    preprocessing = functools.partial(load_preprocess_images, image_size=224)
    wrapper = PytorchWrapper(identifier='clip', model=model, preprocessing=preprocessing)
    wrapper.image_size = 224
    return wrapper

def get_layers(name):
    assert name in all_models
    if name == 'ViT-B/32':
        num_layers = 12
        layers = [f'transformer.resblocks.{i}.ln_2' for i in range(num_layers)]
    elif name == 'RN50':
        layers = CLIP_RN50_LAYERS
    return layers

def get_bibtex(model_identifier):
    return """@article{radford2learning,
                    title={Learning Transferable Visual Models From Natural Language Supervision},
                    author={Radford, Alec and Kim, Jong Wook and Hallacy, Chris and Ramesh, Aditya and Goh, Gabriel and Agarwal, Sandhini and Sastry, Girish and Askell, Amanda and Mishkin, Pamela and Clark, Jack and others},
                    journal={Image},
                    volume={2},
                    pages={T2}}"""


if __name__ == '__main__':
    check_models.check_base_models(__name__)
    #name = 'ViT-B/32'
    #name = 'RN50'
    #get_model(name)
