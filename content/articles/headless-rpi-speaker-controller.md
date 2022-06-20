BOM

Requirements:
Multiple user headless control

BOM
| Brand | Model | Quantity |
|------| ----|-----|
|N/A | US AC Power | 3 |
| Yamaha  | HS7 | 2 | 

Connection Diagram

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