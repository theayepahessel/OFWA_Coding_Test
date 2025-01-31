from flask import Flask, jsonify, request, render_template
import flask
from collections import defaultdict

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('galamsay_analysis.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/analysis', methods=['GET'])
def get_latest_analysis():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM analysis_results ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        if result:
            return jsonify({
                'total_sites': result['total_sites'],
                'region_with_most_sites': result['region_with_most_sites'],
                'average_sites_per_region': result['average_sites_per_region'].decode('utf-8') if isinstance(result['average_sites_per_region'], bytes) else result['average_sites_per_region'],
                'timestamp': result['timestamp'] if 'timestamp' in result.keys() else None
            })
        else:
            return jsonify({'error': 'No analysis results found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/analysis/history', methods=['GET'])
def get_analysis_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM analysis_results ORDER BY id DESC')
        results = cursor.fetchall()
        return jsonify([{
            'total_sites': row['total_sites'],
            'region_with_most_sites': row['region_with_most_sites'],
            'average_sites_per_region': row['average_sites_per_region'].decode('utf-8') if isinstance(row['average_sites_per_region'], bytes) else row['average_sites_per_region'],
            'timestamp': row['timestamp'] if 'timestamp' in row.keys() else None
        } for row in results])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/data', methods=['GET'])
def get_raw_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get query parameters
        group_by = request.args.get('group_by', '').lower()
        sort_by = request.args.get('sort', '').lower()
        min_sites = request.args.get('min_sites', type=int)
        region_filter = request.args.get('region')

        # Base query
        query = 'SELECT * FROM galamsay_data'
        params = []

        # Apply filters
        if min_sites is not None:
            query += ' WHERE number_of_sites >= ?'
            params.append(min_sites)
        if region_filter:
            query += ' AND region = ?' if min_sites else ' WHERE region = ?'
            params.append(region_filter)

        # Apply sorting
        if sort_by == 'sites':
            query += ' ORDER BY number_of_sites DESC'
        
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Process results
        if group_by == 'region':
            # Group data by region
            grouped_data = defaultdict(list)
            region_stats = defaultdict(lambda: {'total_sites': 0, 'count': 0})
            
            for row in results:
                region = row['region']
                city_data = {
                    'city': row['city'],
                    'number_of_sites': row['number_of_sites']
                }
                grouped_data[region].append(city_data)
                region_stats[region]['total_sites'] += row['number_of_sites']
                region_stats[region]['count'] += 1

            # Calculate averages and prepare final response
            response_data = {}
            for region in grouped_data:
                response_data[region] = {
                    'cities': sorted(grouped_data[region], key=lambda x: x['number_of_sites'], reverse=True),
                    'statistics': {
                        'total_sites': region_stats[region]['total_sites'],
                        'average_sites': round(region_stats[region]['total_sites'] / region_stats[region]['count'], 2),
                        'city_count': region_stats[region]['count']
                    }
                }
            
            return jsonify({
                'grouped_by_region': response_data,
                'summary': {
                    'total_regions': len(response_data),
                    'total_cities': sum(stats['count'] for stats in region_stats.values()),
                    'total_sites': sum(stats['total_sites'] for stats in region_stats.values())
                }
            })
        else:
            # Return flat list with enhanced information
            return jsonify({
                'data': [{
                    'city': row['city'],
                    'region': row['region'],
                    'number_of_sites': row['number_of_sites']
                } for row in results],
                'summary': {
                    'total_records': len(results),
                    'total_sites': sum(row['number_of_sites'] for row in results),
                    'average_sites_per_city': round(sum(row['number_of_sites'] for row in results) / len(results), 2) if results else 0
                }
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True) 