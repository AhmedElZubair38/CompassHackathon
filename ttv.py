import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video

pipe = DiffusionPipeline.from_pretrained("ali-vilab/text-to-video-ms-1.7b", torch_device=torch.float16, variant="fp16")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()


prompt = "A cat is playing with a ball of yarn."
video_frames = pipe(prompt, num_inference_steps=25).frames

video_path = export_to_video(video_frames, "meow.mp4")

video_name = video_path.replace('/tmp', '')
print('Name: ', video_name)

torch.cuda.empty_cache()