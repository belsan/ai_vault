from llm_wrapper import OLLAMAWrapper



if __name__ == "__main__":
    from llm_wrapper import OLLAMAWrapper

    model = OLLAMAWrapper("gemma4:26b")
    prompt1 = "How to treat a runny nose?"
    prompt2 = "Runny nose, differential diagnosis." 

    print(f"##############")
    print(f"Prompt 1: {prompt1}")
    print(f"##############")
    print(model.ask(prompt1))
    print(f"##############")
    print(f"Prompt 2: {prompt2}")
    print(f"##############")
    print(model.ask(prompt2)) 