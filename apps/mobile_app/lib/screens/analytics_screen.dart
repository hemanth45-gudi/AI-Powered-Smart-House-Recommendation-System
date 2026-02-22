import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fl_chart/fl_chart.dart';
import '../providers/recommendation_provider.dart';

class AnalyticsDashboard extends ConsumerWidget {
  const AnalyticsDashboard({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final summaryAsync = ref.watch(analyticsSummaryProvider);
    final dailyAsync = ref.watch(analyticsDailyProvider);
    final topHousesAsync = ref.watch(analyticsTopHousesProvider);

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text('Analytics Dashboard', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(analyticsSummaryProvider);
          ref.invalidate(analyticsDailyProvider);
          ref.invalidate(analyticsTopHousesProvider);
        },
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // --- KPI Cards ---
            summaryAsync.when(
              data: (data) => _buildKpiGrid(data),
              loading: () => const Center(child: CircularProgressIndicator(color: Colors.blue)),
              error: (e, _) => Text('Error loading summary: $e', style: const TextStyle(color: Colors.red)),
            ),
            const SizedBox(height: 24),

            // --- Daily Interactions Line Chart ---
            _sectionHeader('Interaction Volume (Last 7 Days)'),
            const SizedBox(height: 12),
            dailyAsync.when(
              data: (data) => _buildLineChart(data),
              loading: () => const Center(child: CircularProgressIndicator(color: Colors.blue)),
              error: (e, _) => Text('Error: $e', style: const TextStyle(color: Colors.red)),
            ),
            const SizedBox(height: 24),

            // --- Top Houses Bar Chart ---
            _sectionHeader('Top Houses by Engagement'),
            const SizedBox(height: 12),
            topHousesAsync.when(
              data: (data) => _buildBarChart(data),
              loading: () => const Center(child: CircularProgressIndicator(color: Colors.blue)),
              error: (e, _) => Text('Error: $e', style: const TextStyle(color: Colors.red)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _sectionHeader(String title) => Text(
    title,
    style: const TextStyle(color: Colors.white70, fontSize: 16, fontWeight: FontWeight.bold),
  );

  Widget _buildKpiGrid(Map<String, dynamic> data) {
    final cards = [
      _kpi('Total Users', '${data['total_users']}', Icons.people, Colors.blue),
      _kpi('Active Today', '${data['active_today']}', Icons.today, Colors.green),
      _kpi('Total Events', '${data['total_interactions']}', Icons.bar_chart, Colors.purple),
      _kpi('CTR', '${data['click_through_rate']}%', Icons.ads_click, Colors.orange),
      _kpi('Clicks', '${data['click_count']}', Icons.touch_app, Colors.teal),
      _kpi('Saves', '${data['save_count']}', Icons.bookmark, Colors.pink),
    ];
    return GridView.count(
      crossAxisCount: 3,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisSpacing: 10,
      mainAxisSpacing: 10,
      childAspectRatio: 1.2,
      children: cards,
    );
  }

  Widget _kpi(String label, String value, IconData icon, Color color) {
    return Container(
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      padding: const EdgeInsets.all(12),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: color, size: 24),
          const SizedBox(height: 6),
          Text(value, style: TextStyle(color: color, fontSize: 20, fontWeight: FontWeight.bold)),
          Text(label, style: const TextStyle(color: Colors.white54, fontSize: 11), textAlign: TextAlign.center),
        ],
      ),
    );
  }

  Widget _buildLineChart(List<dynamic> data) {
    final clicks = data.map((d) => FlSpot(data.indexOf(d).toDouble(), (d['clicks'] as int).toDouble())).toList();
    final saves = data.map((d) => FlSpot(data.indexOf(d).toDouble(), (d['saves'] as int).toDouble())).toList();
    final searches = data.map((d) => FlSpot(data.indexOf(d).toDouble(), (d['searches'] as int).toDouble())).toList();

    return Container(
      height: 220,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: const Color(0xFF1E293B), borderRadius: BorderRadius.circular(16)),
      child: LineChart(
        LineChartData(
          gridData: FlGridData(show: true, drawVerticalLine: false, getDrawingHorizontalLine: (_) => FlLine(color: Colors.white12)),
          borderData: FlBorderData(show: false),
          titlesData: FlTitlesData(
            leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 30, getTitlesWidget: (v, _) => Text('${v.toInt()}', style: const TextStyle(color: Colors.white38, fontSize: 10)))),
            bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, getTitlesWidget: (v, _) {
              final d = data[v.toInt()]['date'] as String;
              return Text(d.substring(8), style: const TextStyle(color: Colors.white38, fontSize: 10));
            })),
            rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
            topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
          ),
          lineBarsData: [
            LineChartBarData(spots: clicks, color: Colors.blue, isCurved: true, dotData: FlDotData(show: false), belowBarData: BarAreaData(show: true, color: Colors.blue.withOpacity(0.1))),
            LineChartBarData(spots: saves, color: Colors.pink, isCurved: true, dotData: FlDotData(show: false)),
            LineChartBarData(spots: searches, color: Colors.orange, isCurved: true, dotData: FlDotData(show: false)),
          ],
        ),
      ),
    );
  }

  Widget _buildBarChart(List<dynamic> data) {
    return Container(
      height: 220,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: const Color(0xFF1E293B), borderRadius: BorderRadius.circular(16)),
      child: BarChart(
        BarChartData(
          gridData: FlGridData(show: false),
          borderData: FlBorderData(show: false),
          titlesData: FlTitlesData(
            bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, getTitlesWidget: (v, _) {
              if (v.toInt() >= data.length) return const Text('');
              final title = (data[v.toInt()]['title'] as String);
              return Text(title.length > 8 ? '${title.substring(0, 8)}…' : title, style: const TextStyle(color: Colors.white38, fontSize: 9));
            })),
            leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 28, getTitlesWidget: (v, _) => Text('${v.toInt()}', style: const TextStyle(color: Colors.white38, fontSize: 10)))),
            rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
            topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
          ),
          barGroups: data.asMap().entries.map((e) => BarChartGroupData(
            x: e.key,
            barRods: [BarChartRodData(toY: (e.value['engagement'] as int).toDouble(), gradient: LinearGradient(colors: [Colors.blue.shade300, Colors.purple.shade400], begin: Alignment.bottomCenter, end: Alignment.topCenter), borderRadius: BorderRadius.circular(4), width: 16)],
          )).toList(),
        ),
      ),
    );
  }
}
