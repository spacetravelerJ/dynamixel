# 1. 펌웨어 업로드 도구 다운로드
wget https://github.com/ROBOTIS-GIT/OpenCR-Binaries/raw/master/bootloader/opencr_ld_shell_x86
chmod +x opencr_ld_shell_x86

# 2. usb_to_dxl 바이너리 파일 다운로드
wget https://github.com/ROBOTIS-GIT/OpenCR-Binaries/raw/master/release/1.0.0/usb_to_dxl.bin

./opencr_ld_shell_x86 /dev/ttyACM0 115200 usb_to_dxl.bin 1
