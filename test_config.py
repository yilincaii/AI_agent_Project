#!/usr/bin/env python3
"""测试配置是否正确加载"""

try:
    from config.config import GROQ_API_KEY, OPENWEATHER_API_KEY, TODOIST_API_KEY
    
    print("🔍 测试 API 密钥配置...")
    
    # 检查 GROQ_API_KEY
    if GROQ_API_KEY:
        masked_key = GROQ_API_KEY[:8] + "..." + GROQ_API_KEY[-4:] if len(GROQ_API_KEY) > 12 else "***"
        print(f"✅ GROQ_API_KEY: {masked_key}")
    else:
        print("❌ GROQ_API_KEY: 未设置")
    
    # 检查其他密钥
    if OPENWEATHER_API_KEY:
        print("✅ OPENWEATHER_API_KEY: 已设置")
    else:
        print("⚠️  OPENWEATHER_API_KEY: 未设置")
        
    if TODOIST_API_KEY:
        print("✅ TODOIST_API_KEY: 已设置") 
    else:
        print("⚠️  TODOIST_API_KEY: 未设置")
    
    print("\n🎉 配置测试完成！")
    
except Exception as e:
    print(f"❌ 配置加载失败: {e}")