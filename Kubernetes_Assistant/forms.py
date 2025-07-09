from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, SelectField, StringField
from wtforms.validators import DataRequired


class CreateCodeGenForm(FlaskForm):
    instruction = TextAreaField("Instruction", validators=[DataRequired()])
    result = TextAreaField("Result", render_kw={"class": "auto-resize-textarea"})
    submit = SubmitField(label="Generate Kubernetes Code")


class QuestionForm(FlaskForm):
    question = TextAreaField("Question", validators=[DataRequired()])
    result = TextAreaField("Result", render_kw={"class": "auto-resize-textarea"})
    submit = SubmitField(label="Ask watsonx")


class ReviewForm(FlaskForm):
    code_input = TextAreaField("Kubernetes Code", render_kw={"class": "auto-resize-textarea"},
                               validators=[DataRequired()])
    result = TextAreaField("Result", render_kw={"class": "auto-resize-textarea"})
    submit = SubmitField(label="Review Code")


class ExplainForm(FlaskForm):
    code_input = TextAreaField("Kubernetes Code", render_kw={"class": "auto-resize-textarea"},
                               validators=[DataRequired()])
    result = TextAreaField("Result", render_kw={"class": "auto-resize-textarea"})
    submit = SubmitField(label="Explain Code")


class K8sClusterForm(FlaskForm):
    kubeconfig = FileField('Upload kubeconfig', validators=[DataRequired()])
    upload_button = SubmitField('Connect to Cluster')


class K8sNamespaceForm(FlaskForm):
    cluster_api_url = StringField('Cluster Current Context', render_kw={'readonly': True})
    namespaces = SelectField('Select Namespace', choices=[])
    submit = SubmitField(label='Select Namespace')


class K8sPodsForm(FlaskForm):
    cluster_api_url = StringField('Cluster Current Context', render_kw={'readonly': True})
    namespaces = SelectField('Selected Namespace', choices=[], render_kw={'disabled': True})
    pods = SelectField('Unhealthy Pods', choices=[])
    submit = SubmitField(label='Diagnose with watsonx')
    show_yaml = SubmitField(label="Show YAML definition")
    result = TextAreaField('Result', render_kw={'readonly': True, "class": "auto-resize-textarea"})


class ScanK8sDeploySts(FlaskForm):
    cluster_api_url = StringField('Cluster Current Context', render_kw={'readonly': True})
    namespaces = SelectField('Selected Namespace', choices=[], render_kw={'disabled': True})
    deploysts = SelectField('Select to scan', choices=[])
    submit = SubmitField(label='Scan with watsonx')
    show_yaml = SubmitField(label="Show YAML definition")
    result = TextAreaField('Result', render_kw={'readonly': True, "class": "auto-resize-textarea"})
