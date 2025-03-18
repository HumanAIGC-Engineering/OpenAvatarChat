
from handlers.avatar.liteavatar.model.algo_model import AvatarInitOption
from handlers.avatar.liteavatar.avatar_processor import AvatarProcessor


class AvatarAlgoType:
    SAMPLE = "sample"
    TTS2FACE_CPU = "tts2face_cpu"


class AvatarProcessorFactory:

    @staticmethod
    def create_avatar_processor(algo_type: AvatarAlgoType,
                                init_option: AvatarInitOption) -> AvatarProcessor:
        algo_adapter = None
        if algo_type == AvatarAlgoType.SAMPLE:
            from tests.inttest.avatar.sample_adapter import SampleAdapter
            algo_adapter = SampleAdapter()
        if algo_type == AvatarAlgoType.TTS2FACE_CPU:
            from handlers.avatar.liteavatar.algo.tts2face_cpu_adapter import Tts2faceCpuAdapter
            algo_adapter = Tts2faceCpuAdapter()
        return AvatarProcessor(algo_adapter, init_option)
