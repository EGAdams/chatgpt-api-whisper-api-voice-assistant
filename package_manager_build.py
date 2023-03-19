import gradio as gr
import openai, config, subprocess
openai.api_key = config.OPENAI_API_KEY

messages = [{"role": "system", "content": 'You are a programming assistant. \
You are an expert in the Swift programming language. \
You are also an expert in the Python programming language.  When writing scripts, \
you prefer using the Python language \
I am trying to create a small swift command line test for educational purposes. \
I am using the linux subsystem for Windows 10. Respond to all input in 1000 words or less. '}]

def transcribe( textFromTextbox):
    global messages
    
    audio = None
    
    print( "textFromTextbox: " + textFromTextbox )
    if (audio is None):
        # get the text from the textbox input
        messages.append({ "role": "user", "content": textFromTextbox })
    else:
        print("Audio received")
        audio_file = open(audio, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        messages.append({ "role": "user", "content": transcript["text"] })

    # get the response from the gpt-3 model and limit the response to 25 words
    response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=messages, max_tokens=50 )
    
    

    system_message = response["choices"][0]["message"]
    
    messages.append(system_message)

    # subprocess.call(["say", system_message['content']])
    # print the system_message['content'] to the console
    print( system_message['content'] )

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

# add a gr.Interface with a microphone and text input and a text output
# This is the command used for making an interface with the gradio library: 
# ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch() 
# It only shows a record icon and a microphone input. 
# I need a microphone source AND a textbox source. will you modify this python code
# so that it will also show a textbox input? 
# ui =
# ui = gr.Interface(fn=transcribe, inputs=[gr.Audio(source="microphone", type="filepath"), gr.inputs.Textbox()], outputs="text")
ui = gr.Interface(fn=transcribe, inputs=[gr.inputs.Textbox()], outputs="text")
# ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()



ui.launch()