from langchain_ollama import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import config, time

llm = OllamaLLM(model=config.model, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), temperature=config.temperature)

def save_to_file(task_nr, content):
    with open(f"zad{task_nr}.html", 'w') as file:
        file.write(content)
        print("Zapisano")

def main():
    all_tasks_done = False
    while not all_tasks_done:
        start = time.time()
        task = input("Please provide a task: ")
        if task.lower() == "exit":
            all_tasks_done = True
            break
        zadanie = llm.invoke(config.template + task + "Pamiętaj o instrukcjach")
        while True:
            if input("Czy odpowiedź spełnia wymagania? y/n: ") == 'y':
                save_to_file(input("Podaj numer zadania: "), zadanie)
                llm.invoke("Zapomnij poprzednią konwersację. Odpowiedz tylko 'ok'")
                czas = time.time() - start
                print(f"Brawo, wykonałeś zadanie w {czas}, prawdopodobnie wykonałbyś to szybciej samemu leniwy debilu")
                break
            else:
                zadanie = llm.invoke(input("Podaj co trzeba naprawić: "))

if __name__ == "__main__":
    main()