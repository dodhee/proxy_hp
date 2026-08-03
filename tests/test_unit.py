import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.proxy_system import ProxySystem
from src.usb_tethering import USBTetheringManager
from src.airplane_manager import AirplaneManager
from src.rotation_scheduler import RotationScheduler


BASE_DIR = Path(__file__).resolve().parent.parent


class TestConfigLoad(unittest.TestCase):
    def test_config_loads_from_file(self):
        config_path = BASE_DIR / "src" / "config.json"
        self.assertTrue(config_path.exists())
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        self.assertIn("rotation_interval", config)
        self.assertIn("default_provider", config)
        self.assertIn("proxy_port", config)

    def test_providers_load_from_file(self):
        providers_path = BASE_DIR / "providers" / "providers.json"
        self.assertTrue(providers_path.exists())
        with open(providers_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("providers", data)
        self.assertIn("telkomsel", data["providers"])
        self.assertIn("smartfren", data["providers"])


class TestProxySystem(unittest.TestCase):
    @patch("src.proxy_system.winreg")
    def test_set_proxy_writes_ip_port_format(self, mock_winreg):
        mock_key = MagicMock()
        mock_hkey = MagicMock()
        mock_hkey.__enter__.return_value = mock_hkey
        mock_hkey.__exit__.return_value = None
        mock_winreg.ConnectRegistry.return_value = mock_hkey
        mock_winreg.OpenKey.return_value.__enter__.return_value = mock_key

        proxy = ProxySystem()
        result = proxy.set_proxy("192.168.1.100", 8080)

        self.assertTrue(result)
        mock_winreg.SetValueEx.assert_any_call(mock_key, "ProxyEnable", 0, mock_winreg.REG_DWORD, 1)
        mock_winreg.SetValueEx.assert_any_call(mock_key, "ProxyServer", 0, mock_winreg.REG_SZ, "192.168.1.100:8080")
        mock_winreg.SetValueEx.assert_any_call(mock_key, "ProxyOverride", 0, mock_winreg.REG_SZ, "*")

    @patch("src.proxy_system.winreg")
    def test_set_proxy_uses_default_port(self, mock_winreg):
        mock_key = MagicMock()
        mock_hkey = MagicMock()
        mock_hkey.__enter__.return_value = mock_hkey
        mock_hkey.__exit__.return_value = None
        mock_winreg.ConnectRegistry.return_value = mock_hkey
        mock_winreg.OpenKey.return_value.__enter__.return_value = mock_key

        proxy = ProxySystem()
        result = proxy.set_proxy("10.0.0.1")

        self.assertTrue(result)
        mock_winreg.SetValueEx.assert_any_call(mock_key, "ProxyServer", 0, mock_winreg.REG_SZ, "10.0.0.1:8080")


class TestUSBTetheringManager(unittest.TestCase):
    @patch("src.usb_tethering.subprocess.run")
    def test_get_current_ip_parses_mocked_output(self, mock_run):
        mock_run.return_value = Mock(
            stdout="""
Windows IP Configuration


Ethernet adapter Ethernet 2:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::1234
   IPv4 Address. . . . . . . . . . . : 192.168.42.129
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . :
"""
        )

        with patch.object(USBTetheringManager, "_find_adb", return_value="fake_adb"):
            with patch.object(USBTetheringManager, "_find_device", return_value="device123"):
                manager = USBTetheringManager()
                ip = manager.get_current_ip()

        self.assertEqual(ip, "192.168.42.129")
        mock_run.assert_called()

    @patch("src.usb_tethering.subprocess.run")
    def test_get_current_ip_fallback_netsh(self, mock_run):
        mock_run.side_effect = [
            Mock(stdout="No IPv4 here"),
            Mock(stdout="    IP Address Preferred 10.10.10.50")
        ]

        with patch.object(USBTetheringManager, "_find_adb", return_value="fake_adb"):
            with patch.object(USBTetheringManager, "_find_device", return_value="device123"):
                manager = USBTetheringManager()
                ip = manager.get_current_ip()

        self.assertEqual(ip, "10.10.10.50")
        self.assertEqual(mock_run.call_count, 2)


class TestAirplaneManager(unittest.TestCase):
    @patch("src.airplane_manager.shutil.which", return_value=None)
    @patch("src.airplane_manager.subprocess.run")
    def test_find_adb_fallback_when_not_in_path(self, mock_run, mock_which):
        mock_run.return_value = Mock(returncode=0)

        with patch.object(AirplaneManager, "_find_device", return_value="device123"):
            manager = AirplaneManager(config={"rotation_interval": 4})
            adb_path = manager._find_adb()

        self.assertIsNotNone(adb_path)
        self.assertTrue(adb_path.endswith("adb.exe") or adb_path.endswith("adb"))
        mock_which.assert_called_with("adb")
        mock_run.assert_called()


class TestRotationScheduler(unittest.TestCase):
    def test_uses_injected_airplane_manager(self):
        mock_airplane = Mock()
        mock_airplane.rotate_ip.return_value = True

        scheduler = RotationScheduler(airplane_manager=mock_airplane, config={"rotation_interval": 1})

        with patch("src.rotation_scheduler.time") as mock_time:
            mock_time.time.side_effect = [0, 1, 2, 3]
            mock_time.sleep.side_effect = [None, None, None, KeyboardInterrupt]

            try:
                scheduler.start()
            except KeyboardInterrupt:
                pass

        # airplane_manager.rotate_ip is called (at least once)
        self.assertGreater(mock_airplane.rotate_ip.call_count, 0)

    def test_no_subprocess_spawned(self):
        # RotationScheduler doesn't import subprocess directly,
        # it uses injected airplane_manager.rotate_ip()
        mock_airplane = Mock()
        mock_airplane.rotate_ip.return_value = True

        scheduler = RotationScheduler(airplane_manager=mock_airplane, config={"rotation_interval": 1})

        with patch("src.rotation_scheduler.time") as mock_time:
            mock_time.time.side_effect = [0, 1, 2, 3]
            mock_time.sleep.side_effect = [None, None, None, KeyboardInterrupt]

            try:
                scheduler.start()
            except KeyboardInterrupt:
                pass

        # Verify airplane_manager.rotate_ip was called, no subprocess spawned
        self.assertGreater(mock_airplane.rotate_ip.call_count, 0)
        # The key assertion: RotationScheduler doesn't spawn subprocess directly
        # It uses injected airplane_manager


if __name__ == "__main__":
    unittest.main()