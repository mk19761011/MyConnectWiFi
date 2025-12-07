import platform
from typing import List, Optional


class WiFiManager:
    """Wi-Fiスキャンと接続管理クラス
    
    Note: Android環境では実際のWi-Fi操作を行いますが、
    開発環境（Windows/Mac等）ではモックデータを返します。
    """
    
    def __init__(self):
        self.platform = platform.system()
        self.is_android = self.platform == "Android"
    
    def scan_networks(self) -> List[str]:
        """利用可能なWi-Fiネットワークをスキャン
        
        Returns:
            SSID名のリスト
        """
        if self.is_android:
            return self._scan_networks_android()
        else:
            # 開発環境用のモックデータ
            return self._scan_networks_mock()
    
    def _scan_networks_android(self) -> List[str]:
        """Android環境でのWi-Fiスキャン
        
        Note: subprocessを使ってシステムのWi-Fi情報を取得します
        """
        try:
            import subprocess
            
            # 方法1: iw または wpa_cli コマンドを試す
            try:
                result = subprocess.run(
                    ['su', '-c', 'iw', 'dev', 'wlan0', 'scan'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    # SSIDを抽出
                    ssids = []
                    for line in result.stdout.split('\n'):
                        if 'SSID:' in line:
                            ssid = line.split('SSID:')[1].strip()
                            if ssid and ssid not in ssids:
                                ssids.append(ssid)
                    if ssids:
                        return ssids
            except Exception as e:
                print(f"Method 1 failed: {e}")
            
            # 方法2: wpa_cliを試す
            try:
                result = subprocess.run(
                    ['wpa_cli', 'scan'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if result.returncode == 0:
                    # スキャン結果を取得
                    result = subprocess.run(
                        ['wpa_cli', 'scan_results'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        ssids = []
                        lines = result.stdout.split('\n')[1:]  # ヘッダーをスキップ
                        for line in lines:
                            parts = line.split()
                            if len(parts) >= 5:
                                ssid = ' '.join(parts[4:])
                                if ssid and ssid not in ssids:
                                    ssids.append(ssid)
                        if ssids:
                            return ssids
            except Exception as e:
                print(f"Method 2 failed: {e}")
            
            # どちらも失敗した場合、開発用モックデータを返す
            print("Wi-Fi scanning not available, using mock data")
            return self._scan_networks_mock()
            
        except Exception as e:
            print(f"Wi-Fiスキャンエラー: {e}")
            return self._scan_networks_mock()
    
    def _scan_networks_mock(self) -> List[str]:
        """開発環境用のモックスキャン"""
        return [
            "MyHome_5G",
            "MyHome_2G",
            "Office_WiFi",
            "Cafe_FreeWiFi",
            "Guest_Network"
        ]
    
    def connect_to_network(self, ssid: str, password: str) -> bool:
        """指定のWi-Fiネットワークに接続
        
        Args:
            ssid: 接続先のSSID
            password: パスワード
            
        Returns:
            接続成功した場合True
        """
        if self.is_android:
            return self._connect_to_network_android(ssid, password)
        else:
            return self._connect_to_network_mock(ssid, password)
    
    def _connect_to_network_android(self, ssid: str, password: str) -> bool:
        """Android環境でのWi-Fi接続
        
        Note: Android 10以降では、プログラムによるWi-Fi接続が制限されています。
        代わりに、設定画面を開いてユーザーに接続を促す方式を採用します。
        """
        try:
            # Android実装（将来的に実装）
            # from jnius import autoclass
            # Intent = autoclass('android.content.Intent')
            # Settings = autoclass('android.provider.Settings')
            # PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            # intent = Intent(Settings.ACTION_WIFI_SETTINGS)
            # PythonActivity.mActivity.startActivity(intent)
            
            return False
        except Exception as e:
            print(f"Wi-Fi接続エラー: {e}")
            return False
    
    def _connect_to_network_mock(self, ssid: str, password: str) -> bool:
        """開発環境用のモック接続"""
        print(f"[Mock] Wi-Fi接続試行: {ssid}")
        # 開発環境では常に成功とする
        return True
    
    def get_current_network(self) -> Optional[str]:
        """現在接続中のWi-FiネットワークのSSIDを取得
        
        Returns:
            接続中のSSID、接続していない場合はNone
        """
        if self.is_android:
            return self._get_current_network_android()
        else:
            return self._get_current_network_mock()
    
    def _get_current_network_android(self) -> Optional[str]:
        """Android環境での現在の接続情報取得"""
        try:
            # Android実装（将来的に実装）
            return None
        except Exception as e:
            print(f"現在のネットワーク取得エラー: {e}")
            return None
    
    def _get_current_network_mock(self) -> Optional[str]:
        """開発環境用のモック"""
        # 開発中は "MyHome_2G" に接続していると仮定
        return "MyHome_2G"
    
    def open_wifi_settings(self):
        """Wi-Fi設定画面を開く
        
        Android 10以降では、直接接続する代わりに設定画面を開いて
        ユーザーに接続を促します。
        """
        if self.is_android:
            self._open_wifi_settings_android()
        else:
            print("[Mock] Wi-Fi設定画面を開きます")
    
    def _open_wifi_settings_android(self):
        """Android環境でWi-Fi設定画面を開く"""
        try:
            # Android実装（将来的に実装）
            pass
        except Exception as e:
            print(f"設定画面オープンエラー: {e}")
