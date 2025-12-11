def test_calculation_stats_endpoint(client):
    """Integration test for GET /calculations/stats"""
    # Create several calculations
    client.post('/calculations', json={"a": 1, "b": 2, "type": "Add"})
    client.post('/calculations', json={"a": 3, "b": 4, "type": "Multiply"})
    client.post('/calculations', json={"a": 10, "b": 2, "type": "Divide"})

    resp = client.get('/calculations/stats')
    assert resp.status_code == 200
    data = resp.json()
    assert data['total_count'] >= 3
    assert 'counts_by_type' in data
    counts = data['counts_by_type']
    assert counts.get('Add', 0) >= 1
    assert counts.get('Multiply', 0) >= 1
    assert counts.get('Divide', 0) >= 1
