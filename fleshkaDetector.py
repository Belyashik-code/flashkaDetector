import subprocess
import re

class FlashDetector:

    def ubuntu_get_flash_info(self) -> list:
        """
        :return: list of lists, every sub-list consists of:
            [0] - string / disk name
            [1] - string / disk size
            [2] - string / used disk space
            [3] - string / free disk space
            [4] - string / used percent
            [5] - string / path where disk was mounted (if path consist spaces, it wil be in [6], [7] or more till the end)
        """
        # получаем список дисков в системе
        lsblk = subprocess.Popen('lsblk', stdout=subprocess.PIPE, shell=True)
        output, err = lsblk.communicate()
        output = re.findall(r"sd\w\s+[^\\]+", str(output))
        flash_drive = []
        result = []
        # отдельяем флешки
        for disk in output:
            # получаем значение поля removable device ('1' - True, '0' - False), если '1' записываем устройство в массив флешек
            if disk.split()[2] == '1':
                flash_drive.append(disk.split()[0])
                print(disk.split()[0])

        # получаем размер, свободное и занятое место для каждой флешки
        df = subprocess.Popen('df', stdout=subprocess.PIPE, shell=True)
        output, err = df.communicate()
        for flashka in flash_drive:
            print(re.search(r"{}.\s+[^\\]+".format(flashka), str(output)))
            flashka_info = re.search(r"{}.\s+[^\\]+".format(flashka), str(output)).group(0)
            result.append(flashka_info.split())

        return result

