import logging
import time
import openai 
from dotenv import find_dotenv, load_dotenv 
from datetime import datetime


load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

client= openai.OpenAI()
model = "gpt-3.5-turbo"

# # # ==  Create our Assistant (Uncomment this to create your assistant) ==
# programmer_assis = client.beta.assistants.create(
#     name="Programmer",
#     instructions="""You are efficient programmer in C++, Java and python. You like to solve different problems with DSA. 
# You also help others in coding in different ways. """,
#      model=model
#  )
# asistant_id = programmer_assis.id
# print(asistant_id)


# === Thread  ===
thread = client.beta.threads.create(
     messages=[
         {
            "role": "user",
            "content": "How do I get started working out to lose fat and build muscles?",
         }
     ]
)
thread_id = thread.id
print(thread_id)

# === Hardcode or ids ===
asistant_id ="asst_AOkR3Dda7ymbVslH8wXrpaDj"
thread_id = "thread_JdiZcWyLaPt5y0rkIvZ2SdH3"

# ==== Create a Message ====
message = "Best way to learn coding?"
message = client.beta.threads.messages.create(
    thread_id=thread_id, 
    role="user", 
    content=message
)

# === Run our Assistant ===
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=asistant_id,
    instructions="Please address the user as Guido",
)


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread_id, 
    run_id=run.id)
print(f"Steps---> {run_steps.data[0]}")
