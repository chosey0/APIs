from interface.kis.messages import SubscribeMessage
print(SubscribeMessage(approval_key="test", stock_code="test", tr_id="test").to_dict())