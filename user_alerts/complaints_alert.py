#!/usr/bin/env python3
# -*- coding: utf_8 -*-

from mypylib.mypylib import get_timestamp
from utils import get_adnl_text, collect_template


class ComplaintsAlert:
	def __init__(self, local, toncenter, *args, **kwargs):
		self.local = local
		self.toncenter = toncenter
		self.create_time = get_timestamp()
		self.timeoute = 604800 # 7 day
	#end define

	def check(self, user):
		past_validation_cycle = self.toncenter.get_validation_cycle(past=True)
		complaints_list = self.toncenter.get_complaints_list(past_validation_cycle.cycle_id)
		for complaint in complaints_list:
			if complaint.is_passed != True:
				continue
			if complaint.adnl_addr in user.get_adnl_list():
				self.warn(user, complaint)
	#end define

	def warn(self, user, complaint):
		alert_id = f"{type(self).__name__}-{complaint.election_id}-{complaint.adnl_addr}"
		triggered_alerts_list = user.get_triggered_alerts_list()
		if alert_id in triggered_alerts_list:
			return
		#end if
		
		adnl_short = get_adnl_text(user, complaint.adnl_addr)
		penalty = complaint.suggested_fine // 10**9
		alert_text = collect_template(self.local, "complaints_alert", adnl=complaint.adnl_addr, adnl_short=adnl_short, election_id=complaint.election_id, penalty=penalty)
		user.add_message(alert_text)
		triggered_alerts_list[alert_id] = get_timestamp()
	#end define

	def warn_old(self, user, complaint):
		alert_name = f"{type(self).__name__}-{complaint.election_id}-{complaint.adnl_addr}"
		triggered_alerts_list = user.get_triggered_alerts_list()
		if alert_name in triggered_alerts_list:
			return
		#end if
		
		adnl_text = get_adnl_text(user, complaint.adnl_addr)
		fine = complaint.suggested_fine // 10**9
		alert_text = "The validator has been fined:" + '\n'
		alert_text += "```" + '\n'
		alert_text += f"ADNL: {adnl_text}" + '\n'
		alert_text += f"election: {complaint.election_id}" + '\n'
		alert_text += f"fine: {fine} TON" + '\n'
		alert_text += "```"
		user.add_message(alert_text)
		triggered_alerts_list[alert_name] = get_timestamp()
	#end define
#end class
