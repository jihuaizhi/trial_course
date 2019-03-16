{
  "course_built": 1,              #课件属性 固定为1，含义为系统内置课件
  "course_name": "kejian名称",    #课件名称
  "course_type": 2,               #课件标识 1 教学类 2实训类
  "course_style": 3,              #课件类别  1 文本类 2 视频类 3 虚拟机类
  "course_status": 1,             #课件状态 固定为1 含义为可用状态
  "course_difficulty": 3,         #课件难度 1 一星 2 二星 3 三星
  "course_description": "阿斯达岁的\n",  #课件描述
  "course_direction_uuid": "e3e2a1c0-13df-11e9-8f56-ff6b73128375",        #课件方向 参考下列字典数据
  "course_direction_type_uuid": "e3e39a10-13df-11e9-acab-fbae6cef836b",   #课件分类  参考下列字典数据
  "course_period": 30,            #推荐课时 单位分钟 0<n<999
  "doc_name": "linux性能监控.mp4",           #文本类课件的文件名
  "doc_path": "/doc/linux性能监控.mp4",      #文本类课件的文件路径（含文件名）
  "video_name": "linux性能监控.mp4",         #视频类课件的文件名
  "video_path": "/video/linux性能监控.mp4",  #视频类课件的文件路径（含文件名）
  "exp_name":"",                             #课件的实验名称
  "exp_video_name": "aaa.mp4",               #课件实验的操作视频文件名
  "exp_video_path": "/exp_video/aaa.mp4",    #课件实验的操作视频文件路径（含文件名）
  "exp_doc_name": "aaa.pdf",                 #课件实验手册文件名
  "exp_doc_path": "/exp_doc/aaa.pdf",        #课件实验手册文件路径
  "exp_enclosure_name": "aaa.zip",           #课件实验附件文件名
  "exp_enclosure_path": "",                  #课件实验附件文件路径
  "exp_images": [                            #课件实验镜像
    {
      "image_file": "/image/aaa.ova"         #课件实验镜像文件名
    },
    {
      "image_file": "/image/bbb.qcow2"
    }
  ]
}