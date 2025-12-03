import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class StatusFlags:
    """Wi-Fi接続ステータスフラグ"""
    ignore_today: bool = False
    ignore_until_manual_reset: bool = False
    last_ignored_date: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class WiFiConfig:
    """Wi-Fi設定情報モデル"""
    ssid: str
    password: str
    priority: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status_flags: StatusFlags = field(default_factory=StatusFlags)
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            "id": self.id,
            "ssid": self.ssid,
            "password": self.password,
            "priority": self.priority,
            "status_flags": self.status_flags.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書から生成"""
        status_flags = StatusFlags.from_dict(data.get("status_flags", {}))
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            ssid=data["ssid"],
            password=data["password"],
            priority=data["priority"],
            status_flags=status_flags
        )
    
    def should_ignore_today(self) -> bool:
        """今日は無視するべきか判定"""
        if not self.status_flags.ignore_today:
            return False
        
        # 日付が変わっていればフラグをリセット
        if self.status_flags.last_ignored_date:
            last_date = datetime.fromisoformat(self.status_flags.last_ignored_date).date()
            today = datetime.now().date()
            if last_date < today:
                self.status_flags.ignore_today = False
                self.status_flags.last_ignored_date = None
                return False
        
        return True
    
    def should_ignore_permanently(self) -> bool:
        """永続的に無視するべきか判定"""
        return self.status_flags.ignore_until_manual_reset
    
    def set_ignore_today(self):
        """今日だけ無視フラグをセット"""
        self.status_flags.ignore_today = True
        self.status_flags.last_ignored_date = datetime.now().isoformat()
    
    def set_ignore_permanently(self, enabled: bool):
        """永続的に無視フラグをセット/解除"""
        self.status_flags.ignore_until_manual_reset = enabled
    
    def is_ignored(self) -> bool:
        """接続候補から除外されているか"""
        return self.should_ignore_today() or self.should_ignore_permanently()
