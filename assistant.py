from flask import Flask, request, jsonify
import traceback 
from openai import OpenAI
import time
client = OpenAI()

thread = client.beta.threads.create()
app = Flask(__name__)

@app.route('/api/assistant/', methods=['POST'])
def process_message():
    try:
        data = request.get_json()
        content = data['content']

        message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content

        )
        run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_eQa3WZuOwOzciJWNnncPj4vL",
        )
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )
        print(messages)
        response_content=next((msg.content[0].text.value for msg in messages.data if msg.role == "assistant"), None)

                


        
        


        # Get the content from the request body


        # Process the content as needed (you can add your logic here)

        # For demonstration, we'll just return the same content

        # Return the response
        return jsonify({'content': response_content}), 200

    except Exception as e:
        print(f"Exception: {str(e)}")
        traceback.print_exc()
        # Handle exceptions as needed
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
