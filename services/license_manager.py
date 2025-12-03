from typing import Tuple


class LicenseManager:
    """ローカルライセンス認証管理クラス（Android対応版）"""
    
    def __init__(self):
        """Google Sheets不要のローカル版"""
        pass
    
    async def verify_license(self, license_key: str) -> Tuple[bool, str, int]:
        """ライセンスキーを検証（ローカル版）
        
        Args:
            license_key: ユーザーが入力したライセンスキー
            
        Returns:
            (認証成功, メッセージ, 残りアクティベート可能数)
        """
        # テスト用のライセンスデータ
        test_licenses = {
            "TEST-KEY-001": {"max": 3, "active": 0},
            "TEST-KEY-002": {"max": 5, "active": 4},
            "PRO-2024-WIFI": {"max": 10, "active": 0},
        }
        
        if license_key not in test_licenses:
            return False, "ライセンスキーが無効です", 0
        
        license_data = test_licenses[license_key]
        max_limit = license_data["max"]
        active_count = license_data["active"]
        
        if active_count < max_limit:
            remaining = max_limit - active_count - 1
            message = f"認証成功：このパスワードで残りあと {remaining} 台アクティベート可能です"
            return True, message, remaining
        else:
            return False, "このライセンスキーは使用上限に達しています", 0
