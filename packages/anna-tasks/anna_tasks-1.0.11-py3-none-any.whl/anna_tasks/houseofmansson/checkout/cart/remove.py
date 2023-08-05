events = [
	{
		"type": "hover",
		"target": "#minicart"
	},
	{
		"type": "click",
		"target": "a.delete",
		"required": False
	},
	{
		"type": "click",
		"target": ".action-accept",
		"required": False
	}
]
assertions = [
]

from anna_lib.selenium import events, util, assertions
from anna_lib.task.abstract_task import AbstractTask


class Remove(AbstractTask):
	def before_execute(self):
		pass

	def __execute__(self):
		if util.get_element(self.driver, target='#minicart'):
			events.hover(self.driver, target='#minicart')
		if util.get_element(self.driver, target='a.delete'):
			events.click(self.driver, target='a.delete')
		if util.get_element(self.driver, target='a.action-accept'):
			events.click(self.driver, target='a.action-accept')

	def after_execute(self):
		pass
