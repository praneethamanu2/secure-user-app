def test_reports_history_endpoint(client):
    """Integration test for GET /reports/history"""
    # create a few calculations
    client.post('/calculations', json={"a": 1, "b": 2, "type": "Add"})
    client.post('/calculations', json={"a": 3, "b": 4, "type": "Multiply"})
    client.post('/calculations', json={"a": 10, "b": 2, "type": "Divide"})

    resp = client.get('/reports/history?limit=2')
    assert resp.status_code == 200
    data = resp.json()
    assert 'total' in data
    assert data['total'] >= 3
    assert 'items' in data
    assert isinstance(data['items'], list)
    assert len(data['items']) == 2
