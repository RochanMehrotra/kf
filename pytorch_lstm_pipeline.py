import kfp

def task(volume,
         step_name='mlp_task'
         ):
    
    return kfp.dsl.ContainerOp(
        name=step_name,
        image='rochanmehrotra/testing_kf:pytorch_lstm',
        command=['python3', '/component/src/task.py'],
        pvolumes={mount_output_to: volume}
    )

@kfp.dsl.pipeline(name='mlp pipeline', description='')
def mlp_pipeline(
        rok_url,
        pvc_size='1Gi'):
    
    vop = kfp.dsl.VolumeOp(
        name='create-volume',
        resource_name='pytorch_pipeline',
        annotations={"rok/origin": rok_url},
        size=pvc_size
    )
    
    component_1 = task(
        volume=vop.volume
    )
    
    if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(mlp_pipeline, 'pytorch_pipeline.tar.gz')
    


