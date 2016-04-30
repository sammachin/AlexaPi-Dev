global nav_token, streamurl, streamid
if debug: print("{}Processing Request Response...{}".format(bcolors.OKBLUE, bcolors.ENDC))
nav_token = ""
streamurl = ""
streamid = ""
print r.content
if r.status_code == 200:
	data = "Content-Type: " + r.headers['content-type'] +'\r\n\r\n'+ r.content
	msg = email.message_from_string(data)		
	for payload in msg.get_payload():
		if payload.get_content_type() == "application/json":
			j =  json.loads(payload.get_payload())
			if debug: print("{}JSON String Returned:{} {}".format(bcolors.OKBLUE, bcolors.ENDC, json.dumps(j)))
		elif payload.get_content_type() == "audio/mpeg":
			filename = path + "tmpcontent/"+a.get('Content-ID').strip("<>")+".mp3" 
			with open(filename, 'wb') as f:
				f.write(payload.get_payload())
		else:
			if debug: print("{}NEW CONTENT TYPE RETURNED: {} {}".format(bcolors.WARNING, bcolors.ENDC, payload.get_content_type()))
	# Now process the response
		for directive in j['messageBody']['directives']:
			if directive['namespace'] == 'SpeechSynthesizer':
				if directive['name'] == 'speak':
					play_audio(path + "tmpcontent/"+directive['payload']['audioContent'].lstrip("cid:")+".mp3")
				elif directive['name'] == 'listen':
					#listen for input - need to implement silence detection for this to be used.
					if debug: print("{}Further Input Expected, timeout in: {} {}ms".format(bcolors.OKBLUE, bcolors.ENDC, directive['payload']['timeoutIntervalInMillis']))
			elif directive['namespace'] == 'AudioPlayer':
				#do audio stuff - still need to honor the playBehavior
				if directive['name'] == 'play':
				nav_token = directive['payload']['navigationToken']
				for stream in directive['payload']['audioItem']['streams']
					if stream['progressReportRequired']:
						streamid = stream['streamId']
					playBehavior = directive['payload']['playBehavior']
					pThread = threading.Thread(target=play_audio, args=(stream['streamUrl'], stream['offsetInMilliseconds']))
					pThread.start()
	return
elif r.status_code == 204:
	GPIO.output(rec_light, GPIO.LOW)
	for x in range(0, 3):
		time.sleep(.2)
		GPIO.output(plb_light, GPIO.HIGH)
		time.sleep(.2)
		GPIO.output(plb_light, GPIO.LOW)
	if debug: print("{}Request Response is null {}(This is OKAY!){}".format(bcolors.OKBLUE, bcolors.OKGREEN, bcolors.ENDC))
else:
	print("{}(process_response Error){} Status Code: {}".format(bcolors.WARNING, bcolors.ENDC, r.status_code))
	r.connection.close()
	GPIO.output(lights, GPIO.LOW)
	for x in range(0, 3):
		time.sleep(.2)
		GPIO.output(rec_light, GPIO.HIGH)
		time.sleep(.2)
		GPIO.output(lights, GPIO.LOW)