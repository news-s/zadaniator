try:
    from langchain_ollama import OllamaLLM
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    import config, time
except:
    import os, sys
    os.system("pip install requirements.txt")
    print("Please run program agian")
    sys.exit(1)

llm = OllamaLLM(model=config.model, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), temperature=config.temperature)

def save_code_file(task_nr, content):
    with open(f"zad{task_nr}_kod.html", 'w') as file:
        file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kod</title>
</head>
<body>
    <textarea style="width: 400px; height:850px;">
        {content}
    </textarea>
</body>
</html>

""")
        print("Zapisano")

def save_to_file(task_nr, content):
    start = content.find("```") + 3
    end = content.find("```", start)
    code = content[start:end].strip()
    with open(f"zad{task_nr}.html", 'w') as file:
        file.write(code)
        print("Zapisano")

def main():
    all_tasks_done = False
    while not all_tasks_done:
        start = time.time()
        task = input("Please provide a task: ")
        if task.lower() == "exit":
            all_tasks_done = True
            break
        zadanie = llm.invoke(config.template + task + " Pamiętaj o instrukcjach")
        while True:
            if input("Czy odpowiedź spełnia wymagania? y/n: ") == 'y':
                task_nr = input("Podaj numer zadania: ")
                save_to_file(task_nr, zadanie)
                if input("Czy trzeba wykonać plik z kodem źródłowym?: ").lower() == 'y':
                    save_code_file(task_nr, zadanie)
                llm.invoke("Zapomnij poprzednią konwersację. Odpowiedz tylko 'ok'")
                print("\n")
                czas = time.time() - start
                print(f"Brawo, wykonałeś zadanie w {czas}, prawdopodobnie wykonałbyś to szybciej samemu leniwy debilu")
                break
            else:
                zadanie = llm.invoke(input("Podaj co trzeba naprawić: "))

if __name__ == "__main__":
    main()