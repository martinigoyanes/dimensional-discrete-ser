import torch.optim as optim
from torch.optim import lr_scheduler
import torch
from torch import nn
from utils import *
from SpeechDataset import *
from Network import *
from train import *
from experiment import *

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
dataset = "iemocap"
path = f"/Users/martin/Documents/UNIVERSIDAD/CLASES/4º/2o Cuatri/TFG/code/data/{dataset}"
iemocap = {
    0: "ang",
    1: "hap",
    2: "sad",
    3: "neu",
    4: "fru",
    5: "exc",
    6: "fea",
    7: "sur",
    8: "dis",
    9: "oth"
}
msp = {
    0: "A", 
    1: "H", 
    2: "S", 
    3: "N", 
    4: "C", 
    5: "F", 
    6: "U", 
    7: "D", 
    8: "O"
}
if dataset == "iemocap":
    classes = iemocap
else:
    classes = msp

results = {
    "train": {
        "v_ccc": [],
        "a_ccc": [],
        "d_ccc": [],
        "ccc": [],
        "cat_loss": [],
        "dim_loss": [],
    },
    "val": {
        "v_ccc": [],
        "a_ccc": [],
        "d_ccc": [],
        "ccc": [],
        "loss": [],
        "cat_loss": [],
        "dim_loss": [],
    },
}
data = {
    "classes": classes, 
    "vocab_size": 2913,  # msp: 26590  iemocap: 2913 or 3438  
    "audio_feat": "paa+compare.npy",
    "text_feat": "text_seq_73_lemmas.npy",
    "labels_cat": "emotions.npy",
    "labels_dim": "dimension.npy",
    "embeddings": f"{path}/embeddings_lemmas.npy",
    "ratio": {
        "train": 0.65,
        "val": 0.15,
    },
}
params = {
    "name": "parallel",
    "audio_net": {
        "timesteps": 1,
        "feature_size": 198,
        "hidden_size": (256, 256, 256),
        "dropout": 0.3,
    },
    "text_net": {
        "embed_dim": 300,
        "timesteps": 73,
        "hidden_size": (256, 256, 256),
        "output_size": 64,
        "dropout": 0.3,
    },
    "net": {"hidden_size": (64, 32), "dropout": 0.4},
}

learning = {
    "test_bsz": 2048,    # "test_bsz": 2048,
    "train_bsz": 64,  # 64/128 good 
    "lr": 0.001,
    "scheduler": {"step": 7, "gamma": 0.1},
    "loss": {"alpha": 0.7, "beta": 0.2, "gamma": 0.1},
    "epochs": 100,
    "patience": 10,
    "delta": 0.0001,
    "seed": None,  # {"rn": 123, "np": 99, "torch": 1234},
}
num_runs = 1

crit_cat = nn.CrossEntropyLoss() # (weight=weights)
crit_dim = CCCLoss(
    learning["loss"]["alpha"],
    learning["loss"]["beta"],
    learning["loss"]["gamma"],
).to(device)

experiment(learning, params, data, device, path, crit_cat, crit_dim, num_runs=num_runs)

# dataset, dataloader = load_data(
#     data["classes"],
#     data["audio_feat"],
#     data["text_feat"],
#     data["labels_cat"],
#     data["labels_dim"],
#     path,
#     params['text_net']['timesteps'],
#     params['audio_net']['timesteps'],
#     data["ratio"]["train"],
#     data["ratio"]["val"],
#     learning["train_bsz"],
#     learning["test_bsz"],
# )

# crit_dim = CCCLoss(
#     learning["loss"]["alpha"],
#     learning["loss"]["beta"],
#     learning["loss"]["gamma"],
# ).to(device)

# # most_common, _ = torch.max(torch.FloatTensor([v[1] for emo, v in dataset['train'].imbalances.items()]), dim=0)
# # weights = torch.FloatTensor([most_common/v[1] for emo, v in dataset['train'].imbalances.items()]).to(device)
# # print(weights)
# crit_cat = nn.CrossEntropyLoss() # (weight=weights)

# # pretty_print(dataset["all"], dataset["train"], dataset["val"], dataset["test"])

# model = create_network(
#     learning["train_bsz"],
#     data["vocab_size"],
#     data["embeddings"],
#     params["audio_net"],
#     params["text_net"],
#     params["net"],
#     len(dataset["all"].classes),
#     device,
# )
# print(model)

# # Usaremos Adam para optimizar
# optimizer_ft = optim.RMSprop(model.parameters(), lr=learning["lr"])

# exp_lr_scheduler = lr_scheduler.StepLR(
#     optimizer_ft,
#     step_size=learning["scheduler"]["step"],
#     gamma=learning["scheduler"]["gamma"],
# )

# print("-" * 50)
# print("\t\t\tTRAINING")
# print("-" * 50)

# train_model(
#     model,
#     learning["seed"],
#     params["name"],
#     dataset,
#     device,
#     dataloader,
#     crit_cat,
#     crit_dim,
#     optimizer_ft,
#     exp_lr_scheduler,
#     results,
#     learning["epochs"],
#     learning["patience"]
# )

# # plot_training(results, params["name"])

# model.load_state_dict(torch.load(f'{params["name"]}.pt'))

# test_model(model, crit_cat, crit_dim, dataloader["test"], dataset["test"], device)