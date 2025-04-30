# Frontend package.json Update for Testing

To add testing capabilities to your frontend, you'll need to update your `package.json` file. Here's what you should add:

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  },
  "devDependencies": {
    "@testing-library/vue": "^8.0.2",
    "@vue/test-utils": "^2.4.5",
    "happy-dom": "^13.8.6",
    "vitest": "^1.4.0"
  }
}
```

To update your package.json, run the following commands in your frontend directory:

```bash
npm install --save-dev @testing-library/vue @vue/test-utils happy-dom vitest
```

Then add the test scripts to your package.json file.
