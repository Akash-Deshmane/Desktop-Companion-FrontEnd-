import 'package:flutter/material.dart';

class SettingsScreen extends StatefulWidget {
  final bool isDarkMode;
  final Function(bool) onThemeChanged;

  final String appName;
  final Function(String) onNameChanged;

  const SettingsScreen({
    super.key,
    required this.isDarkMode,
    required this.onThemeChanged,
    required this.appName,
    required this.onNameChanged,
  });

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late TextEditingController controller;

  @override
  void initState() {
    super.initState();
    controller = TextEditingController(text: widget.appName);
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Settings")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Appearance",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 10),

            // 🔹 Dark Mode Toggle
            SwitchListTile(
              title: const Text("Dark Mode"),
              value: widget.isDarkMode,
              onChanged: (value) {
                widget.onThemeChanged(value);
              },
            ),

            const SizedBox(height: 30),

            const Text(
              "Application Settings",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 10),

            // 🔹 App Name Field
            TextField(
              controller: controller,
              decoration: const InputDecoration(
                labelText: "Application Name",
                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 10),

            ElevatedButton(
              onPressed: () {
                widget.onNameChanged(controller.text.trim());

                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("App name updated")),
                );
              },
              child: const Text("Save"),
            ),
          ],
        ),
      ),
    );
  }
}
