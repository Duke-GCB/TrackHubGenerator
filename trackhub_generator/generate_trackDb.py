import yaml
import argparse

from jinja2 import Environment, PackageLoader


def render_template(yaml_object, template_name):
    env = Environment(loader=PackageLoader(package_name='trackhub_generator'))
    template = env.get_template(template_name + '.j2')
    print template.render(yaml_object)


def main(yaml_file_name, template_name):
    with open(yaml_file_name) as yaml_file:
        obj = yaml.load(yaml_file)
        render_template(obj,template_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file', type=argparse.FileType('r'))
    parser.add_argument('template_name')
    parser.add_argument_group()
    args = parser.parse_args()
    main(args.yaml_file.name, args.template_name)
