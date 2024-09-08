<template>
  <div id="app" class="container">
    <h1>Text Comparison Tool</h1>
    <div class="input-area">
      <textarea v-model="text1" placeholder="Paste or type text here"></textarea>
      <textarea v-model="text2" placeholder="Paste or type text here"></textarea>
    </div>
    <div class="controls">
      <button @click="compareTexts">Compare</button>
      <button @click="clearTexts">Clear</button>
      <button @click="toggleOptions">Options</button>
    </div>
    <div v-if="comparisonResults" class="results">
      <h3>Comparison Results</h3>
      <div v-for="(line, index) in comparisonResults" :key="index">
        <span :class="line.type">{{ line.text }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text1: '',
      text2: '',
      comparisonResults: null,
      showOptions: false
    };
  },
  methods: {
    compareTexts() {
      // Simulate comparison - Replace with actual API call to the C++ backend
      const lines1 = this.text1.split('\n');
      const lines2 = this.text2.split('\n');
      const maxLength = Math.max(lines1.length, lines2.length);
      const results = [];

      for (let i = 0; i < maxLength; i++) {
        const line1 = lines1[i] || '';
        const line2 = lines2[i] || '';
        
        if (line1 === line2) {
          results.push({ text: line1, type: 'unchanged' });
        } else {
          if (line1) results.push({ text: `- ${line1}`, type: 'removed' });
          if (line2) results.push({ text: `+ ${line2}`, type: 'added' });
        }
      }

      this.comparisonResults = results;
    },
    clearTexts() {
      this.text1 = '';
      this.text2 = '';
      this.comparisonResults = null;
    },
    toggleOptions() {
      this.showOptions = !this.showOptions;
      alert('Options feature is not implemented yet!');
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  text-align: center;
}

.input-area {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

textarea { 
  width: 100%;
  height: 150px;
  padding: 10px;
  font-size: 16px;
}

.controls {
  margin-bottom: 20px;
}

button {
  padding: 10px 15px;
  margin: 0 5px;
  cursor: pointer;
}

.results {
  text-align: left;
}

.results .added {
  color: green;
  font-weight: bold;
}

.results .removed {
  color: red;
  font-weight: bold;
}

.results .unchanged {
  color: black;
}
</style>
