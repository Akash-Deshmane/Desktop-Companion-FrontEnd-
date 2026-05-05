import 'package:flutter/material.dart';
import '../models/message.dart';
import 'chat_screen.dart';
import 'history_screen.dart';
import 'settings_screen.dart';

class DashboardScreen extends StatefulWidget {
  final bool isDarkMode;
  final Function(bool) onThemeChanged;
  final String appName;
  final Function(String) onNameChanged;

  const DashboardScreen({
    super.key,
    required this.isDarkMode,
    required this.onThemeChanged,
    required this.appName,
    required this.onNameChanged,
  });

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  // 🔥 SINGLE SOURCE OF TRUTH
  List<Message> messages = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.appName)),

      drawer: Drawer(
        child: ListView(
          children: [
            const DrawerHeader(
              child: Text("Menu", style: TextStyle(fontSize: 18)),
            ),

            // 🔹 Dashboard
            ListTile(
              leading: const Icon(Icons.dashboard),
              title: const Text("Dashboard"),
              onTap: () => Navigator.pop(context),
            ),

            // 🔹 Chat History (PASS DATA)
            ListTile(
              leading: const Icon(Icons.history),
              title: const Text("Chat History"),
              onTap: () {
                Navigator.pop(context); // close drawer

                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => HistoryScreen(
                      history: messages, // ✅ FIXED
                    ),
                  ),
                );
              },
            ),

            // 🔹 Settings
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text("Settings"),
              onTap: () {
                Navigator.pop(context);

                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => SettingsScreen(
                      isDarkMode: widget.isDarkMode,
                      onThemeChanged: widget.onThemeChanged,
                      appName: widget.appName,
                      onNameChanged: widget.onNameChanged,
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),

      body: Center(
        child: ElevatedButton.icon(
          icon: const Icon(Icons.chat),
          label: const Text("Start Chat"),
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => ChatScreen(
                  messages: messages, // ✅ FIXED
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
