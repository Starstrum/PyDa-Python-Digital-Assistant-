import wx
import wikipedia
import wolframalpha
import pyttsx3
import pyaudio
import speech_recognition as sr

#The course I followed can be found at https://www.udemy.com/course/learn-python-build-a-virtual-assistant-in-python/learn/lecture/4854468?start=0#overview
#initialize python text to speech engine
engine = pyttsx3.init()
engine.say("Welcome")
engine.runAndWait()

class MyFrame(wx.Frame):
	#constructor method
	#def is usedto make methods __init__ is the constructor method
	def __init__(self):
		wx.Frame.__init__(self, None,
			pos=wx.DefaultPosition, size=wx.Size(450,100),
			style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
			wx.CLOSE_BOX | wx.CLIP_CHILDREN,
			title = "PyDa")
		panel = wx.Panel(self)
		#subwindows in a window is a sizer
		#sizer is an abstract class so you have to use one of the concrete classes++
		my_sizer = wx.BoxSizer(wx.VERTICAL)
		lbl = wx.StaticText(panel,
		label="Hello I am Pyda the Python Digital Assistant. How can I help you?")
		my_sizer.Add(lbl,0,wx.ALL,5)
		#textbox
		self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
		self.txt.SetFocus()
		self.txt.Bind(wx.EVT_TEXT_ENTER,self.OnEnter)
		my_sizer.Add(self.txt,0,wx.ALL,5)
		panel.SetSizer(my_sizer)
		self.Show()

	#method definition
	def OnEnter(self,event):
		input = self.txt.GetValue()
		input.lower()
		#if no input use speech recognizer
		if input == '':
			r = sr.Recognizer()
			with sr.Microphone() as source:
				audio = r.listen(source)
			try:
				self.txt.SetValue(r.recognize_google(audio))
			except sr.UnknownValueError:
				print ("Google Speech Recognition could not understand audio")
			except sr.RequestError as e:
				print ("Could not request results from Google Speech Recognition service")
		try:
			#wolframalpha
			app_id = "L9UTQL-R9V5XXK2A5"
			client = wolframalpha.Client(app_id)
			result = client.query(input)
			answer = next(result.results).text
			print(answer)
			engine.say(answer)
			engine.runAndWait()
		except:
			#wikipedia
			#split the input by spaces to take care of who is, what is, what are questions
			#take the last two words as input
			#another try except incase the question isnt what is or what are
			try:
				input = input.split(' ')
				input = " ".join(input[2:])
				print(wikipedia.summary(input))
				engine.say(wikipedia.summary(input))
				engine.runAndWait()
			except:
				input = self.txt.GetValue()
				input = input.lower()
				print(wikipedia.summary(input))
				engine.say(wikipedia.summary(input))
				engine.runAndWait()

#main method __name__ is a special variable
if __name__ == "__main__":
	app = wx.App(True)
	fram = MyFrame()
	app.MainLoop()