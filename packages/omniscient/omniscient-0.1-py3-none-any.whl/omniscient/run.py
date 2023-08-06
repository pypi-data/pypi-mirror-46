from deeppavlov import build_model, configs


def predict(model, context, question):
    print(model(['I have six bananas'], ['How many banans do I have']))
    return model([context], [question])


def run():
    print("Hello World!")

    model = build_model(configs.squad.squad, download=True)
    ans = model(['DeepPavlov is library for NLP and dialog systems.'], ['What is DeepPavlov?'])

    print('deeppavlov ans output', ans)

    return model


if __name__ == '__main__':
    run()
