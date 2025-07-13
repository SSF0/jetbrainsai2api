#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版代理启动脚本
让Python项目通过Clash代理访问外网
"""

import os
import sys
import subprocess
import socket


def check_proxy_port(host="localhost", port=7890):
    """检查代理端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def test_proxy_connection(proxy_url):
    """测试代理连接"""
    try:
        print("🔍 测试代理连接...")
        import httpx
        with httpx.Client(timeout=8.0) as client:
            response = client.get("https://httpbin.org/ip")
            if response.status_code == 200:
                ip_info = response.json()
                print(f"✅ 代理连接正常，外网IP: {ip_info.get('origin', 'Unknown')}")
                return True
            else:
                print(f"⚠️  代理响应异常: HTTP {response.status_code}")
                return False
    except Exception as e:
        print(f"⚠️  代理连接测试失败: {e}")
        return False


def main():
    proxy_url = "http://localhost:7890"  # Clash HTTP代理地址
    target_file = "main.py"              # 要启动的文件
    
    print("🚀 启动jetbrainsai2api项目...")
    print(f"📡 HTTP代理: {proxy_url}")
    print("-" * 50)
    
    # 1. 检查代理端口
    if not check_proxy_port():
        print("❌ 代理端口7890无法连接")
        print("💡 请确保Clash正在运行且HTTP代理已开启")
        return
    
    print("✅ 代理端口连接正常")
    
    # 2. 设置代理环境变量
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    os.environ['http_proxy'] = proxy_url
    os.environ['https_proxy'] = proxy_url
    os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1'
    os.environ['no_proxy'] = 'localhost,127.0.0.1,::1'
    
    # 3. 测试代理连接
    proxy_ok = test_proxy_connection(proxy_url)
    
    if not proxy_ok:
        print("⚠️  代理测试失败，可能原因:")
        print("   • Clash节点选择了SOCKS5代理（请切换到HTTP模式）")
        print("   • 代理节点连接异常")
        print("   • 网络连接问题")
        choice = input("\n是否继续启动? (y/N): ").lower().strip()
        if choice != 'y':
            print("👋 启动已取消")
            return
    
    # 4. 启动项目
    print("\n🌐 所有HTTP请求将通过Clash代理访问")
    print("📍 服务将在 http://localhost:8002 启动")
    print("⏹️  按 Ctrl+C 停止服务")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, target_file], env=os.environ.copy())
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except FileNotFoundError:
        print(f"\n❌ 文件不存在: {target_file}")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")


if __name__ == "__main__":
    main()