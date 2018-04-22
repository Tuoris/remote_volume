# This script is slightly modified version of
# Himanshu dua answer at
# https://stackoverflow.com/questions/25631123/programmatically-changing-system-wide-speaker-balance-on-windows-7

from comtypes import GUID, IUnknown, STDMETHOD, COMMETHOD, HRESULT, c_float
import comtypes.client
from ctypes import POINTER
from ctypes.wintypes import DWORD, BOOL

MMDeviceApiLib = \
    GUID('{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
IID_IMMDevice = \
    GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
IID_IMMDeviceEnumerator = \
    GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
CLSID_MMDeviceEnumerator = \
    GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
IID_IMMDeviceCollection = \
    GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
IID_IAudioEndpointVolume = \
    GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')


class IMMDeviceCollection(IUnknown):
    _iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
    pass


class IAudioEndpointVolume(IUnknown):
    _iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
    _methods_ = [
        STDMETHOD(HRESULT, 'RegisterControlChangeNotify', []),
        STDMETHOD(HRESULT, 'UnregisterControlChangeNotify', []),
        STDMETHOD(HRESULT, 'GetChannelCount', []),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], POINTER(GUID), 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], POINTER(GUID), 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
                  (['out', 'retval'], POINTER(c_float), 'pfLevelDB')
                  ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
                  (['out', 'retval'], POINTER(c_float), 'pfLevelDB')
                  ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
                  (['in'], DWORD, 'nChannel'),
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], POINTER(GUID), 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
                  (['in'], DWORD, 'nChannel'),
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], POINTER(GUID), 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
                  (['in'], DWORD, 'nChannel'),
                  (['out', 'retval'], POINTER(c_float), 'pfLevelDB')
                  ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
                  (['in'], DWORD, 'nChannel'),
                  (['out', 'retval'], POINTER(c_float), 'pfLevelDB')
                  ),
        COMMETHOD([], HRESULT, 'SetMute',
                  (['in'], BOOL, 'bMute'),
                  (['in'], POINTER(GUID), 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'GetMute',
                  (['out', 'retval'], POINTER(BOOL), 'pbMute')
                  ),
        COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
                  (['out', 'retval'], POINTER(c_float), 'pnStep'),
                  (['out', 'retval'], POINTER(c_float), 'pnStepCount'),
                  ),
        COMMETHOD([], HRESULT, 'VolumeStepUp',
                  (['in'], POINTER(GUID), 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'VolumeStepDown',
                  (['in'], POINTER(GUID), 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'QueryHardwareSupport',
                  (['out', 'retval'], POINTER(DWORD), 'pdwHardwareSupportMask')
                  ),
        COMMETHOD([], HRESULT, 'GetVolumeRange',
                  (['out', 'retval'], POINTER(c_float), 'pfMin'),
                  (['out', 'retval'], POINTER(c_float), 'pfMax'),
                  (['out', 'retval'], POINTER(c_float), 'pfIncr')
                  ),

    ]


class IMMDevice(IUnknown):
    _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'Activate',
                  (['in'], POINTER(GUID), 'iid'),
                  (['in'], DWORD, 'dwClsCtx'),
                  (['in'], POINTER(DWORD), 'pActivationParans'),
                  (['out', 'retval'], POINTER(
                      POINTER(IAudioEndpointVolume)), 'ppInterface')
                  ),
        STDMETHOD(HRESULT, 'OpenPropertyStore', []),
        STDMETHOD(HRESULT, 'GetId', []),
        STDMETHOD(HRESULT, 'GetState', [])
    ]
    pass


class IMMDeviceEnumerator(comtypes.IUnknown):
    _iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')

    _methods_ = [
        COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
                  (['in'], DWORD, 'dataFlow'),
                  (['in'], DWORD, 'dwStateMask'),
                  (['out', 'retval'], POINTER(
                      POINTER(IMMDeviceCollection)), 'ppDevices')
                  ),
        COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
                  (['in'], DWORD, 'dataFlow'),
                  (['in'], DWORD, 'role'),
                  (['out', 'retval'], POINTER(POINTER(IMMDevice)), 'ppDevices')
                  )
    ]


class Volume:
    def __init__(self):
        self._enumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER
        )

        self._endpoint = self._enumerator.GetDefaultAudioEndpoint(0, 1)
        self._volume = self._endpoint.Activate(IID_IAudioEndpointVolume,
                                               comtypes.CLSCTX_INPROC_SERVER, None)

    def get_volume_level(self):
        self._internal_level = self._volume.GetMasterVolumeLevelScalar() * 100
        return round(self._internal_level)

    def set_volume_level(self, value=50):
        if value not in range(0, 100+1):
            return

        self._internal_level = value / 100
        return self._volume.SetMasterVolumeLevelScalar(self._internal_level, None)

    def get_mute(self):
        return bool(self._volume.GetMute())

    def mute(self):
        return self._volume.SetMute(True, None)

    def un_mute(self):
        return self._volume.SetMute(False, None)

    level = property(get_volume_level, set_volume_level)


def main():
    volume = Volume()
    current_level = volume.get_volume_level()
    volume.set_volume_level(current_level)
    is_muted = volume.get_mute()
    if is_muted:
        volume.mute()
    else:
        volume.un_mute()
    volume.un_mute


if __name__ == '__main__':
    main()
