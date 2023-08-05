# -*- coding: utf-8 -*-
DESC = "ocr-2018-11-19"
INFO = {
  "IDCardOCR": {
    "params": [
      {
        "name": "ImageBase64",
        "desc": "图片的BASE64值。\n支持的图片格式：PNG、JPG、JPEG，暂不支持GIF格式。\n支持的图片大小：所下载图片经Base64编码后不超过6M。图片下载时间不超过3秒。\n图片的 ImageUrl、ImageBase64必须提供一个，如果都提供，只使用ImageBase64。"
      },
      {
        "name": "ImageUrl",
        "desc": "图片URL地址。\n支持的图片格式：PNG、JPG、JPEG，暂不支持GIF格式。\n支持的图片大小：所下载图片经Base64编码后不超过3M。图片下载时间不超过3秒。\n图片存储于腾讯云的Url可保障更高下载速度和稳定性，建议图片存储于腾讯云。非腾讯云存储的Url速度和稳定性可能受一定影响。"
      },
      {
        "name": "CardSide",
        "desc": "FRONT为身份证有照片的一面（正面）\nBACK为身份证有国徽的一面（反面）"
      },
      {
        "name": "Config",
        "desc": "可选字段，根据需要选择是否请求对应字段。\n目前包含的字段为：\nCropIdCard-身份证照片裁剪，bool类型，\nCropPortrait-人像照片裁剪，bool类型，\nCopyWarn-复印件告警，bool类型，\nReshootWarn-翻拍告警，bool类型。\n\nSDK设置方式参考：\nConfig = Json.stringify({\"CropIdCard\":true,\"CropPortrait\":true})\nAPI 3.0 Explorer设置方式参考：\nConfig = {\"CropIdCard\":true,\"CropPortrait\":true}"
      }
    ],
    "desc": "身份证识别接口支持二代身份证正反面所有字段的识别，包括姓名、性别、民族、出生日期、住址、公民身份证号、签发机关、有效期限；具备身份证照片、人像照片的裁剪功能和翻拍件、复印件的识别告警功能。应用场景包括：银行开户、用户注册、人脸核身等各种身份证信息有效性核验场景。"
  },
  "GeneralFastOCR": {
    "params": [
      {
        "name": "ImageBase64",
        "desc": "图片的BASE64值。\n支持的图片格式：PNG、JPG、JPEG，暂不支持GIF格式。\n支持的图片大小：所下载图片经Base64编码后不超过3M。图片下载时间不超过3秒。\n图片的 ImageUrl、ImageBase64必须提供一个，如果都提供，只使用ImageBase64。"
      },
      {
        "name": "ImageUrl",
        "desc": "图片的URL地址。\n支持的图片格式：PNG、JPG、JPEG，暂不支持GIF格式。\n支持的图片大小：所下载图片经Base64编码后不超过3M。图片下载时间不超过3秒。\n图片存储于腾讯云的Url可保障更高下载速度和稳定性，建议图片存储于腾讯云。非腾讯云存储的Url速度和稳定性可能受一定影响。"
      }
    ],
    "desc": "通用印刷体识别（高速版）接口用于提供图像整体文字的检测和识别服务，返回文字框位置与文字内容。相比通用印刷体识别接口，识别速度更快、支持的QPS更高。"
  },
  "GeneralBasicOCR": {
    "params": [
      {
        "name": "ImageBase64",
        "desc": "图片的BASE64值。\n支持的图片格式：PNG、JPG、JPEG，暂不支持GIF格式。\n支持的图片大小：所下载图片经Base64编码后不超过3M。图片下载时间不超过3秒。\n图片的 ImageUrl、ImageBase64必须提供一个，如果都提供，只使用ImageBase64。"
      },
      {
        "name": "ImageUrl",
        "desc": "图片的URL地址。\n支持的图片格式：PNG、JPG、JPEG，暂不支持GIF格式。\n支持的图片大小：所下载图片经Base64编码后不超过3M。图片下载时间不超过3秒。\n图片存储于腾讯云的Url可保障更高下载速度和稳定性，建议图片存储于腾讯云。非腾讯云存储的Url速度和稳定性可能受一定影响。"
      },
      {
        "name": "Scene",
        "desc": "保留字段。"
      }
    ],
    "desc": "通用印刷体识别接口用于提供图像整体文字的检测和识别服务，返回文字框位置与文字内容。支持多场景、任意版面下整图文字的识别，以及中英文、字母、数字和日文、韩文的识别。应用场景包括：印刷文档识别、网络图片识别、广告图文字识别、街景店招识别、菜单识别、视频标题识别、头像文字识别等。"
  }
}