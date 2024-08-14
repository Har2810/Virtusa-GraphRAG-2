# GRAPHRAG WITHOUT OPEN AI

We will be implementing Microsoft's GraphRag Technology but instead of using OPEN AI API Keys, we will be using a model from groq as our inference model and nomic-embed-text from ollama for the embeddings.
We will be incorporating Gradio and Fast API as part of our tech stack.

- Firstly create a folder named *input* in your directory and add the .txt file which contains your large text content on the basis of which you would ask your queries to get a response.

- Get the api key from [ Groq.com](https://console.groq.com/keys) and store it safely on your system

- Head over to the official website to get the link to  [Download Ollama](https://ollama.com/download/linux) and paste it in the terminal 

- Open the terminal in the same directory as your *input* folder and type -
  
  ```
  $ ollama pull nomic-embed-text
  ```

- To install graphrag, type -
  
  ```
  $ pip install graphrag
  ```

- export the groq api key -
  
  ```
  $ export GRAPHRAG_API_KEY = <your_groq_api_key>
  ```

- To initialize we then run this command -
  
  ```
  python3 -m graphrag.index --root .
  ```
  
  The above command would generate a number of files and folders which would be visible to you on your vs code along with the *input* folder

- Open the newly added *settings.yaml* file in the editor and change the following  things  under `llm:`-

```
model: mixtral-8x7b-32768
api_base: https://api.groq.com/openai/v1

tokens_per_minute: 3000 # set a leaky bucket throttle
requests_per_minute: 30 # set a leaky bucket throttle
max_retries: 3
max_retry_wait: 10.0
```

- Then under `embeddings:` change the following- 

```
model: nomic_embed_text
api_base: https://localhost:11434/api
```

- Go to the terminal and type (this is an unsupported method or hack to get the nomic-embed-text work locally)

```
$ sudo find / -name openai_embeddings_llm.py
```

The above will give you the path of the *openai_embeddings_llm.py* file. Hover over the path and open it in editor

- make the following  changes to this file - Add `import ollama` in the code. Then  scroll towards the end and replace the last portion with -

```
embedding_list = []
        for inp in input:
            embedding = ollama.embeddings(model="nomic-embed-text", prompt=inp)
            embedding_list.append(embedding["embedding"])
        return embedding_list
```

- Now go to the terminal and run the following command-

```
$ python3 -m graphrag.index --root .
```

- Then run the below command to run the *main.py* file which enables the Gradio UI

```
$ python3 -main.py
```

Open  browser and go to the url : http://localhost:8000 and ask your question.


**NOTE:**

- Works only for global search

- Had used document on Pixel 8  - made it a smaller file of 12kb

- Will be slow or not work if too big of a file used

- Since its a global search , answers to specific questions closely related to a specific portion of the document aren't answered correctly. May also include hallucinations. 


  
  
