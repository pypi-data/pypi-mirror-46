from torchwisdom.vision.trainer.supervise import *

if __name__ == '__main__':
    from torchwisdom.vision.models import mobilenetv2
    from torchvision.datasets.mnist import MNIST
    import torchvision.transforms as transforms
    from torchwisdom.core.utils.data import DatasetCollector
    import torch.optim as optim
    import torch.nn as nn

    train_path = '/data/MNIST/train'
    valid_path = '/data/MNIST/valid'

    tmft = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor()
    ])

    trainset = MNIST(train_path, train=True, transform=tmft, download=False)
    validset = MNIST(valid_path, train=False, transform=tmft, download=False)

    data = DatasetCollector(trainset, validset)
    model = mobilenetv2(pretrained=False, in_chan=1)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, )
    scheduler = StepLRCallback(optimizer, step_size=30)

    trainer = ConvTrainer(data=data, model=model, criterion=criterion, optimizer=optimizer, callbacks=[scheduler])
    trainer.fit(1)

    # print(data.bunch())
    # print()
    # test(name='fandi')
