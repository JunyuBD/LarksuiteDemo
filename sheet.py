import lark

token = "WDm5sD2GVhSl45tR7XguqQchsHk"
sheet_id = "a00cc6"
cell_range = "a00cc6!A1:B2"

lark.api_user('sheets/v3/spreadsheets/' + token + '/sheets/' + sheet_id + '/values/' + cell_range + '/insert', 'post', {
	"values": [
		[
			[
				{
					"type": "text",
					"text": {
						"text": "ABC"
					}
				}
			],
			[
				{
					"type": "value",
					"value": {
						"value": 123352
					}
				}
			]
		],
		[
			[
				{
					"type": "value",
					"value": {
						"value": "1233"
					}
				}
			],
			[
				{
					"type": "value",
					"value": {
						"value": 123352
					}
				}
			]
		]
	]
})