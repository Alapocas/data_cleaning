from pyhanlp import HanLP, JClass
PerceptronLexicalAnalyzer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')
PerceptronSegmenter = JClass('com.hankcs.hanlp.model.perceptron.PerceptronSegmenter')
PerceptronPOSTagger = JClass('com.hankcs.hanlp.model.perceptron.PerceptronPOSTagger')
analyzer = PerceptronLexicalAnalyzer()
seg = PerceptronSegmenter()
tag = PerceptronPOSTagger()