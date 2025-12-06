import json
import os
import base64
from typing import List, Optional
from models.wifi_config import WiFiConfig


class StorageManager:
    """ローカルストレージ管理クラス（Android対応版）"""
    
    def __init__(self, storage_dir: str = None):
        # デフォルトではアプリのデータディレクトリを使用
        if storage_dir is None:
            storage_dir = os.path.join(os.path.expanduser("~"), ".my_connect_wifi")
        
        self.storage_dir = storage_dir
        self.config_file = os.path.join(storage_dir, "config.json")
        
        # ディレクトリが存在しない場合は作成
        try:
            os.makedirs(storage_dir, exist_ok=True)
        except PermissionError:
            # Androidなどで権限がない場合、カレントディレクトリ（アプリ領域）を使用
            storage_dir = os.path.join(os.getcwd(), "app_data")
            self.storage_dir = storage_dir
            self.config_file = os.path.join(storage_dir, "config.json")
            os.makedirs(storage_dir, exist_ok=True)
    
    def _encrypt_password(self, password: str) -> str:
        """パスワードを簡易暗号化（Base64）"""
        return base64.b64encode(password.encode()).decode()
    
    def _decrypt_password(self, encrypted_password: str) -> str:
        """パスワードを復号化"""
        try:
            return base64.b64decode(encrypted_password.encode()).decode()
        except Exception:
            return ""
    
    def load_config(self) -> dict:
        """設定ファイルを読み込む"""
        if not os.path.exists(self.config_file):
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # パスワードを復号化
            for wifi in config.get("wifi_configs", []):
                wifi["password"] = self._decrypt_password(wifi["password"])
            
            return config
        except Exception as e:
            print(f"設定ファイル読み込みエラー: {e}")
            return self._get_default_config()
    
    def save_config(self, config: dict):
        """設定ファイルを保存"""
        # パスワードを暗号化
        config_to_save = config.copy()
        config_to_save["wifi_configs"] = []
        for wifi in config.get("wifi_configs", []):
            wifi_copy = wifi.copy()
            wifi_copy["password"] = self._encrypt_password(wifi["password"])
            config_to_save["wifi_configs"].append(wifi_copy)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_to_save, f, indent=2, ensure_ascii=False)
    
    def _get_default_config(self) -> dict:
        """デフォルト設定を返す"""
        return {
            "user_settings": {
                "scan_interval_seconds": 300,
                "notifications_enabled": True
            },
            "wifi_configs": [],
            "license_info": {
                "is_pro_unlocked": False,
                "activated_keys": []
            }
        }
    
    def get_wifi_configs(self) -> List[WiFiConfig]:
        """Wi-Fi設定リストを取得"""
        config = self.load_config()
        wifi_list = []
        for wifi_data in config.get("wifi_configs", []):
            wifi_list.append(WiFiConfig.from_dict(wifi_data))
        
        # 優先順位でソート
        wifi_list.sort(key=lambda x: x.priority)
        return wifi_list
    
    def save_wifi_configs(self, wifi_configs: List[WiFiConfig]):
        """Wi-Fi設定リストを保存"""
        config = self.load_config()
        config["wifi_configs"] = [wifi.to_dict() for wifi in wifi_configs]
        self.save_config(config)
    
    def add_wifi_config(self, wifi: WiFiConfig):
        """Wi-Fi設定を追加"""
        configs = self.get_wifi_configs()
        configs.append(wifi)
        self.save_wifi_configs(configs)
    
    def delete_wifi_config(self, wifi_id: str):
        """Wi-Fi設定を削除"""
        configs = self.get_wifi_configs()
        configs = [w for w in configs if w.id != wifi_id]
        self.save_wifi_configs(configs)
    
    def update_wifi_config(self, wifi: WiFiConfig):
        """Wi-Fi設定を更新"""
        configs = self.get_wifi_configs()
        for i, w in enumerate(configs):
            if w.id == wifi.id:
                configs[i] = wifi
                break
        self.save_wifi_configs(configs)
    
    def get_license_info(self) -> dict:
        """ライセンス情報を取得"""
        config = self.load_config()
        return config.get("license_info", {
            "is_pro_unlocked": False,
            "activated_keys": []
        })
    
    def save_license_info(self, license_info: dict):
        """ライセンス情報を保存"""
        config = self.load_config()
        config["license_info"] = license_info
        self.save_config(config)
    
    def add_activated_key(self, key: str):
        """アクティベート済みキーを追加（ローカル版）"""
        license_info = self.get_license_info()
        if key not in license_info["activated_keys"]:
            license_info["activated_keys"].append(key)
            license_info["is_pro_unlocked"] = True
            self.save_license_info(license_info)
