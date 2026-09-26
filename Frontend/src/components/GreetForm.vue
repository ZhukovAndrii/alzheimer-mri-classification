<script>
export default {
  data() {
    return {
      name: '',
      diagnose: '',
    };
  },
  methods: {

    async process() {
      try {
        const response = await fetch('http://localhost:5000/process', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: this.name }),
        });
        const data = await response.json();
        this.diagnose = data;
      } catch (error) {
        console.error('Error fetching diagnose:', error);
      }
    },
    
    async uploadImage() {
      if(!this.image) {
        alert('Please selcet an image to upload.')
        return;
      }

      try {
        const formData = new FormData();
        formData.append('image', this.image);

        const response = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const data = await response.json();
          alert('Image uploaded successfully: ' + data.filePath);
        } else {
          alert('Failed to upload image.');
        }
      } catch (error) {
        console.error('Error uploading image:', error);
      }
    },
    
    onFileChange(event) {
      const file = event.target.files[0];
      document.getElementById('fileName').innerText = file ? file.name : 'No file chosen';
      this.image = file;
    }
  },
};
</script>

<template>
  <div>
    <h1>To see result upload x-ray and push the button</h1>
    <div flex gap-2>
      <button @click="process">Get diagnose</button>
    </div>
    <h2 v-if="diagnose">{{ diagnose }}</h2>

    <div grid gap-4>
      <h1>Upload an Image</h1>
      <div>
        <span id="fileName" style="cursor: pointer; padding: 5px; border: 1px solid grey; display: inline-block;">No file chosen</span>
        <label for="fileUpload" style="cursor: pointer; display: inline-block;">
          <img src="@/assets/icons/folder.svg" alt="Upload Icon" style="width: 30px; height: 30px; margin-right: 5px;" />
        </label>
        <input id="fileUpload" type="file" style="display: none;" @change="onFileChange" />
      </div>
      <button @click="uploadImage">
        <img src="@/assets/icons/cloud.svg" alt="Upload Icon" style="width: 50px; height: 20px; margin-right: 5px;" />        
      </button>
    </div>
  </div>
</template>