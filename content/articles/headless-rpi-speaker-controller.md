# Overview
Hi there and welcome to the blog series where I try to get a raspberry pi up and running as a way to control an extra set of powered speakers. I know there are a lot of other pages out there for how to set a system to do something like this, but I think they approach it from a "how to" lens. This series, and blog really, is meant to offer insight into my design process. For a lot of audio and other engineering projects, there isn't always a lot of looking into how to make design decisions or ones that talk about workflow. Additionally "how do" posts tend to lack the very important part of integrating systems: troubleshooting problems. My skill level for a lot of these tools is still in its nancency, but I want to document my learning process in case it helps out someone else. So with that, let's get into the artcle. 

# User Experience
When starting with a project, I like to think of what I want my workflow to be. Here are a few key points I came up with
* I want to listen to music in my bedroom.
* I want multiple people to be able to control the music.
* I want to connect with multiple devices (laptops, phones, tablets, etc).
* I want a chromecast-like experience, meaning users can "cast" to the device.
* I want an experience similiar to my eARC setup in my living room where controller can turn on and off the different components in the system. 
* I wanted to turn the speakers off when they are not in use.

# Constraints
* I must use my existing powered speakers.
* I must use one of my raspberry pis.
* Digital communication should be wireless (controller, internet, etc).
* Setup must be discrete. 
* No TV. 

Bear in mind, these are likely to change along the way. Hopefully I'll figure out a way to show what gets added with future projects, because I think it's really interesting to track. It's important to note that so many things are not known until you try something so it's best to have a quick way to get back to a known state. With the desired user experience and constraints defined. It was time for some research. 

To turn on and off the speakers, a friend told me about [opto-isolated relays](https://en.wikipedia.org/wiki/Opto-isolator). These are the components that are commonly used in AV recievers to saftely turn the power circuitry on/off. Additionally it help separate higher voltages from the system that is recieving the signal. In this application, it means I won't have to expose the raw 120V AC line directly from the socket to the speakers. Instead, I found a powerstrip that can be controlled with the GPIO of the raspberry pi. I found an IoT relay 

BOM

Requirements:
Multiple user headless control

BOM
| Brand | Model | Quantity |
|------| ----|-----|
| N/A | US AC Power | 3 |
| Yamaha  | HS7 | 2 | 
| Raspberry Pi | Model 3 B V1.2 | 1 | 
| Logitech  | Wireless Keyboard and Mouse | 1 |
| Canakit | Powercable | 1 | 
| Sleek socket | Ultra-Thin Electrical Outlet Cover with 3 Outlet Power Strip and Cord Management Kit, 8-Foot, Universal Size  | 1 |
| [Iot Relay - Enclosed High-power Power Relay](https://www.digital-loggers.com/iot2spec.pdf) | DLI | 1 |
Connection Diagram
<Need program that's betters at makeing connection diagram>

Other notes:

Starting and stopping services via bash scripts
how to execute bash scripts via web

Got the bluetooth working on the raspberry pi moode audio. it's great and free. 
need to use commands to turn gpio on and off
shouldn't have set change hte gpio modes
ssh pi@192.168.1.2
raspi-gpio get
raspi-gpio set 25 op dl
raspi-gpio set 25 op dh 

pi@moode:~ $ dmesg | grep sound
[   12.269371] snd-allo-boss-dac soc:sound: snd_soc_register_card() failed: -517
[   12.278587] snd-allo-boss-dac soc:sound: snd_soc_register_card() failed: -517
[   12.736337] snd-allo-boss-dac soc:sound: snd_soc_register_card() failed: -517
[   12.769458] snd-allo-boss-dac soc:sound: snd_soc_register_card() failed: -517
[   13.472209] snd-allo-boss-dac soc:sound: snd_soc_register_card() failed: -517
[   13.478174] snd-allo-boss-dac soc:sound: snd_soc_register_card() failed: -517
[   13.492936] snd-allo-boss-dac soc:sound: snd_soc_register_card() failed: -517

Seems like troubleshooting shows the sound card messing up, likely because i was turning off GPIO

Bluetooth notes: 
1) can have multiple devices  attacheh
2) bluetooth shows where the devices are connected. 
3) get weird audio issues if both try to place at the same time. 

# Soundtrack
[Old Man Gloom - No](https://oldmangloom.bandcamp.com/album/no)

[How to setup netgear static IO](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
[Apache Stepped on the moode audio web service]()
http://192.168.1.1/start.htm
[Raspberry Pi Relay - GPIO Control](https://play.google.com/store/apps/details?id=com.jasonfindlay.pirelaypro&hl=en_IE)
[What the hell is UPnP?](https://en.wikipedia.org/wiki/List_of_UPnP_AV_media_servers_and_clients)
[InnoMaker DAC Hat](https://www.inno-maker.com/product/hifi-dac-hat/)
[MoOde Github setup](https://github.com/moode-player/moode/blob/master/www/setup.txt)
[MoOde Audio Website](https://moodeaudio.org/)
[What is a renderer?](https://community.volumio.org/t/upnp-dlna-renderer/5245) 
[What is bluetooth SBC XQ](https://www.google.com/search?client=firefox-b-1-d&q=+Bluetooth+SBC+XQ)
[Intro to MoOde](https://www.headphonesty.com/2021/09/introduction-to-moode-audio/)
[InnoMaker Manual 1.2](http://www.inno-maker.com/wp-content/uploads/2017/12/HIFI-AMP-HAT-User-Manual-V1.2.pdf)
[More Details about the Pinout](https://www.jianguoyun.com/p/DZUVHxwQpdSrBxi8rZ0B#file=%2FUser%20Manual%2FHIFI%20DAC%20User%20ManualV1.5.pdf::size=7655947)
[GPIO Pinout](https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/#pret%20tyPhoto)

future ideas: project approaches to finding out informaiton 

