from . import fileutil, ifileinfo, utils
import os

class FileWriter:
    def __init__(self,file, mode = 'w'):
        """
            Writes to a file
            Arguments:
                file - Accepts either a fileUtil, or IFileInfo Specialization
                mode - Allows for `w` for writing or `a` for appending
        """
        if(issubclass(type(file),ifileinfo.IFileInfo)):
            self.file = file 
        elif(issubclass(type(file),fileutil.FileUtil)):
            self.file = file.file
        else:
            raise TypeError("Wrong argument type")
        
        self.mode = mode

    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        self.close()
    def close(self):
        self.file.close()
    def create_file(self,new_filepath,samplerate = None):
        """
            Creates a new file with the extension of the current one
            NOTE: In order to normalize, you should run `fileutil.standardize` method
            Arguments:
                data - A multidimensional numpy array(channels x frames)
                new_filepath - The diretory and  name the new file will have, it will convert based on file extension
                samplerate (Optional) - The samplerate the file should have, if not supplied it will use the own `file` samplerate .
        """
        file_exists = (os.path.isfile(new_filepath))
        if(samplerate == None):
            samplerate = self.file.getSamplerate()
        path = utils.path_splitter(new_filepath)
        if(path['name'] == None):
            raise TypeError("It doesn't contain a filename")
        try:
            os.mkdir(path['path'])
            #tries to create the directory
        except OSError as e:
            import errno
            if(e.errno != errno.EEXIST):
                raise #if there's an error thats not eexits(file/directory exists)
            pass
        import soundfile as sf
        if(self.mode == 'a' and file_exists):
            with sf.SoundFile(path['full_path'], mode = 'r+') as wfile:
                wfile.seek(0,sf.SEEK_END)
                wfile.write(self.file.getSamples())
        else:
            sf.write(path['full_path'], self.file.getSamples(), samplerate,format=path['extension']) # writes to the new file 
        return
'''
    def append(self, data_to_add):
        """
            Allows for appending contents to a sound file;
            NOTE:
                It doesn't create a file, the file should be created using create_file method
            Arguments:
                data_to_add: Can be either a IFileInfo subclass or a numpy array
        """
        #check if is IFileInfo descendant or numpy array
        if(issubclass(type(data_to_add),ifileinfo.IFileInfo)):
            data_to_add = data_to_add.getSamples()
        self.file.addSamples(data_to_add)
'''