var apiURL = 'https://api.github.com/repos/kugan49/webosmc/'
var apiBranches = 'branches'
var apiCommits = 'commits?per_page=5&sha='


var GitStatus = new Vue({

  el: '#GitStatus',

  data: {  	
    branches: null,
    currentBranch: 'master',
    commits: null
  },

  created: function () {
    this.fetchData()
  },

  watch: {
    currentBranch: 'fetchData'
  },

  filters: {
    truncate: function (v) {
      var newline = v.indexOf('\n')
      return newline > 0 ? v.slice(0, newline) : v
    },
    formatDate: function (v) {
      return v.replace(/T|Z/g, ' ')
    }
  },
	
  methods: {
    fetchData: function () {
      var xhr1 = new XMLHttpRequest()
      var self1 = this
      
      var getAPI1 =  apiURL + apiBranches
      xhr1.open('GET',getAPI1)
      xhr1.onload = function () {
        var Locbranches = []
        var i
        var ret = JSON.parse(xhr1.responseText)
        for (i = 0; i <  ret.length; i++) {
          Locbranches.push(ret[i].name)
        }
        console.log(Locbranches)
        self1.branches = Locbranches
      }
      xhr1.send()
      var xhr = new XMLHttpRequest()
      var self = this
      xhr.open('GET', apiURL + apiCommits + self.currentBranch)
      xhr.onload = function () {
        self.commits = JSON.parse(xhr.responseText)
        console.log(self.commits)
      }
      xhr.send()
    }
  }
})
