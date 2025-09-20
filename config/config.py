import os
from dotenv import load_dotenv
from pathlib import Path

# 获取项目根目录路径（config文件夹的上一级）
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

# 只调用一次 load_dotenv，指定路径
load_dotenv(dotenv_path=env_path)

# 从环境变量获取 API 密钥
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

FULL_AI_TRACE = False

# 调试：检查是否成功加载
if not GROQ_API_KEY:
    print(f"⚠️  警告：未找到 GROQ_API_KEY，.env 文件路径: {env_path}")
    print(f"⚠️  .env 文件是否存在: {env_path.exists()}")
    # 额外调试信息
    if env_path.exists():
        try:
            with open(env_path, 'r') as f:
                content = f.read()
                print(f"📝 .env 文件内容预览: {content[:100]}...")
        except Exception as e:
            print(f"❌ 读取 .env 文件失败: {e}")
else:
    print("✅ GROQ_API_KEY 加载成功")

# 显示所有加载的环境变量状态
print(f"🔧 调试信息:")
print(f"   - 工作目录: {os.getcwd()}")
print(f"   - .env 路径: {env_path}")
print(f"   - GROQ_API_KEY: {'✅ 已设置' if GROQ_API_KEY else '❌ 未设置'}")
print(f"   - OPENWEATHER_API_KEY: {'✅ 已设置' if OPENWEATHER_API_KEY else '❌ 未设置'}")
print(f"   - TODOIST_API_KEY: {'✅ 已设置' if TODOIST_API_KEY else '❌ 未设置'}")