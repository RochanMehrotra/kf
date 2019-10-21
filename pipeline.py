import kfp

def generate_data(output_uri, output_uri_in_file,
               volume,
               step_name='generate_data',
              mount_output_to='/data'):
    return kfp.dsl.ContainerOp(
        name=step_name,
        image='rochanmehrotra/testing_kf:generate_data',
        arguments=[
            '--output1-path', output_uri,
            '--output1-path-file', output_uri_in_file,
        ],
        command=['python3', '/component/src/data_generator.py'],
        file_outputs={
            'output_file': output_uri,
            'output_uri_in_file': output_uri_in_file,
        },
        pvolumes={mount_output_to: volume}
    )

def train(output_uri, output_uri_in_file,
               volume,
               step_name='train',
              mount_output_to='/data'):
    return kfp.dsl.ContainerOp(
        name=step_name,
        image='rochanmehrotra/testing_kf:train',
        arguments=[
            '--model-path', output_uri,
            '--output1-path-file', output_uri_in_file,
        ],
        command=['python3', '/component/src/train.py'],
        file_outputs={
            'output_file': output_uri,
            'output_uri_in_file': output_uri_in_file,
        },
        pvolumes={mount_output_to: volume}
    )


def evaluate(output_uri, output_uri_in_file,
               volume,
               step_name='train',
              mount_output_to='/data'):
    return kfp.dsl.ContainerOp(
        name=step_name,
        image='rochanmehrotra/testing_kf:train',
        arguments=[
            '--model-path', output_uri,
            '--output1-path-file', output_uri_in_file,
        ],
        command=['python3', '/component/src/evaluate.py'],
        file_outputs={
            'output_file': output_uri,
            'output_uri_in_file': output_uri_in_file,
        },
        pvolumes={mount_output_to: volume}
    )

@kfp.dsl.pipeline(name='mlp pipeline', description='')
def mlp_pipeline(
        rok_url,
        pvc_size='1Gi'):
    
    vop = kfp.dsl.VolumeOp(
        name='create-volume',
        resource_name='mlp_pipeline',
        annotations={"rok/origin": rok_url},
        size=pvc_size
    )
    
    component_1 = generate_data(
        output_uri='/data',
        output_uri_in_file='/data',
        volume=vop.volume
    )
    
    component_2 = train(
        output_uri='/data',
        output_uri_in_file='/data/output1_path_file',
        volume=vop.volume
    )
    
    component_3 = evaluate(
        output_uri='/data',
        output_uri_in_file='/data/output1_path_file',
        volume=vop.volume
    )
    
    if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(mlp_pipeline, 'mlp_pipeline.tar.gz')
    

