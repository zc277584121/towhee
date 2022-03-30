/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  // tutorialSidebar: [{type: 'autogenerated', dirName: '.'}],

  // But you can create a sidebar manually

  doc: [
    'overview',
    {
      'Getting started': [
        'get-started/install',
        'get-started/quick-start',
        'get-started/troubleshooting',
        'get-started/gsoc-2022',
        //'get-started/pipeline-config',
      ],
    },
    {
      Tutorials: [
        'tutorials/image-deduplication',
        'tutorials/music-recognition-system',
        'tutorials/reverse-image-search',
      ],
    },
    {
      'Fine Tune': [
          'fine-tune/train-operators/quick-start',
          'fine-tune/train-operators/fine-tune-with-MNIST',
          'fine-tune/train-operators/train-a-bird-classification-model',
          'fine-tune/train-operators/training-configs',
      ]
    },
    {
      'Supported pipelines': [
        'pipelines/image-embedding',
        'pipelines/audio-embedding',
      ],
    },
    {
      'Developer guides': [
        {
          Contributing: ['developer-guides/contributing/contributing-guide'],
        },
        {
          Framework: [
            'developer-guides/framework/architecture-overview',
            'developer-guides/framework/pipeline-overview',
            'developer-guides/framework/DAG-details',
            'developer-guides/framework/engine-details',
            'developer-guides/framework/dataframe-details',
            // 'developer-guides/framework/layer-subframework',
            'developer-guides/framework/hub-integration-and-caching',
            'developer-guides/framework/image-ensemble-training',
          ],
        },
        {
          Models: ['developer-guides/models/layers-overview'],
        },
      ],
      //'advanced/roadmap',
    },
  ],
};

module.exports = sidebars;
