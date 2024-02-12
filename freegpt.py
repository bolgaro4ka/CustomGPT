import g4f

g4f.debug.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking
print(g4f.version)  # check version
print(g4f.Provider.Ails.params)  # supported args


# Automatic selection of provider
def freegpt(message, model, temperature):
    # streamed completion
    ans = ""
    response = g4f.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": message}],
        tempetarure=temperature,
    )
    for messages in response:
        ans += messages

    return ans


# for message in response:
#    print(message, flush=True, end='')
